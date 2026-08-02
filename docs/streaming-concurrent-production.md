# Streaming production mode

`scripts/run_continuous_production.sh` now runs three resumable stages at the same time:

```text
GitHub crawl -> accepted_repositories.jsonl -> prescreen follower -> pending.jsonl
                                                         -> E2B follower (20 per key)
                                                         -> candidates / tasks
```

The crawl writes each page and accepted record immediately. The prescreen process keeps a
byte cursor at `outputs/github_crawl_500_unquota/accepted_repositories.cursor.json`, so a
restart only replays the unfinished tail. E2B keeps its worker pool alive while pending is
temporarily empty and exits only after the prescreen done marker exists and the queue drains.
If GitHub has no more results in any configured language, the crawler records a completed
partial checkpoint with `exhausted_without_full_target=true`; the available records are still
screened and delivered, and the monitor stops instead of starting empty extension cycles.

The pending buffer uses a high watermark of 480 and resumes intake below 120. This prevents a
fast prescreen stage from creating an unbounded queue while still keeping the three E2B key
lanes supplied. Per-run status files are written under
`outputs/production-runs/<run-id>/`:

- `prescreen-follow.status.json`: cursor, accepted/queued counts, and intake rates;
- `e2b-follow.status.json`: in-flight count for every key slot, capacity reductions, and
  completed verification rate;
- `crawl.status`, `prescreen.status`, and `e2b.status`: process exit codes and completion
  markers.

Local checkouts use `~/.cache/alvance-github-crawler/workspaces` rather than `/tmp`. The
default 50GB quota is divided into 80 reservations of 640MB, allowing 60 E2B workers and 20
prescreen workers to run concurrently while bounding local checkout growth. A repository whose
archive plus expanded tree exceeds one reservation is rejected before extraction.

The monitor reads these files and shows active E2B slots rather than only the configured
maximum. Ctrl+C sends a checkpoint-safe stop to all three stages. Cursors, pending events,
tasks, and logs remain local. The script never pushes Git automatically.

## Manual command

After configuring `.env` with the GitHub token pool, `OPENAI_API_KEY`, and one or more numbered
E2B keys:

```bash
cd /home/xubingyu/AlvanceGithubCrawler
git switch XBY
AUTO_GIT_PUSH=false uv run python monitor.py
```

The command starts the dashboard and the complete crawl -> prescreen -> E2B -> Task pipeline.
Every configured E2B key gets up to 20 workers (for example, two keys provide 40 slots and
three keys provide 60).
Use `Ctrl+C` in the dashboard to pause; run the same command again to resume from the cursor.
When the local run finishes, inspect the generated report and push manually with
`git push origin XBY`.
