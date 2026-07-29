# Pipeline statistics: github-500-unquota-20260729

- Status: `complete`
- Generated: `2026-07-29T12:53:52.387045+00:00`
- Raw GitHub sample: 500
- Initial filter accepted: 239
- E2B queue: 59
- Deliverable tasks: 6
- Pending: 0

## Language funnel

| Language | Initial accepted | Final tasks |
|---|---:|---:|
| python | 54 | 2 |
| go | 65 | 3 |
| typescript | 35 | 0 |
| javascript | 33 | 1 |
| rust | 52 | 0 |

## Stage timings

| Stage | Duration (s) | Exit |
|---|---:|---:|
| crawl | 344 | 0 |
| verify-default-resume | 760 | 0 |
| prebuild-escalated | 1307 | 0 |
| verify-escalated | 798 | 0 |
| verify-rustfs-cache-recovery | 3 | 0 |
| verify-rustfs-final | 538 | 0 |

## E2B task performance

| Repository | Language | Resources | Cold start (s) | Tests (s) | Peak MB | Task |
|---|---|---|---:|---:|---:|---|
| [NSPC911/rovr](https://github.com/NSPC911/rovr) | python | 1 CPU / 1024 MB | 0.42 | 37.47 | 308.3 | `tasks/alv-rovr-462fd8-e8002859-v2` |
| [zhnt/loushang](https://github.com/zhnt/loushang) | python | 1 CPU / 1024 MB | 0.63 | 67.07 | 196.3 | `tasks/alv-loushang-2b9ea9-7ed49fc9-v2` |
| [bitnami/sealed-secrets](https://github.com/bitnami/sealed-secrets) | go | 1 CPU / 1024 MB | 0.45 | 106.06 | 744.1 | `tasks/alv-sealed-secrets-2ab4a1-fb7da1e9-v2` |
| [hetznercloud/hcloud-cloud-controller-manager](https://github.com/hetznercloud/hcloud-cloud-controller-manager) | go | 1 CPU / 1024 MB | 0.48 | 91.86 | 665.8 | `tasks/alv-hcloud-cloud-control-a2a07e-27253f52-v2` |
| [kube-vip/kube-vip](https://github.com/kube-vip/kube-vip) | go | 1 CPU / 1024 MB | 0.39 | 27.91 | 144.5 | `tasks/alv-kube-vip-51d2e4-0d248ba4-v2` |
| [devswha/patina](https://github.com/devswha/patina) | javascript | 1 CPU / 1024 MB | 0.49 | 118.28 | 101.1 | `tasks/alv-patina-6b5b94-b98b3b03-v2` |

## Logs

Raw stage logs are under `outputs/github_production_500_unquota/logs`.
