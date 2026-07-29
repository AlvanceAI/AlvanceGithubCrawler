# Pipeline statistics: github-mass-production-XBY-20260729

- Status: `incomplete`
- Generated: `2026-07-29T20:17:05.615376+00:00`
- Raw GitHub sample: 4500
- Initial filter accepted: 2185
- E2B queue: 534
- Deliverable tasks: 87
- Pending: 0

## Language funnel

| Language | Initial accepted | Final tasks |
|---|---:|---:|
| python | 452 | 8 |
| go | 601 | 47 |
| typescript | 363 | 5 |
| javascript | 234 | 7 |
| rust | 535 | 20 |

## Stage timings

| Stage | Duration (s) | Exit |
|---|---:|---:|
| crawl-1000 | 324 | 0 |
| prescreen-1000 | 335 | 130 |
| verify-default-20260729T142325Z | 289 | 143 |
| prescreen-resume-1000 | 529 | 0 |
| crawl-1500 | 338 | 0 |
| prescreen-1500 | 881 | 0 |
| crawl-2000 | 343 | 0 |
| prescreen-2000 | 114 | 130 |
| verify-default-20260729T151419Z | 1422 | 143 |
| prescreen-resume-2000 | 678 | 0 |
| crawl-2500 | 36 | 1 |
| verify-default-20260729T153842Z | 1221 | 143 |
| prescreen-resume-2500 | 126 | 0 |
| crawl-3000 | 643 | 0 |
| prescreen-3000 | 2396 | 0 |
| crawl-3500 | 331 | 0 |
| prescreen-3500 | 1548 | 0 |
| crawl-4000 | 339 | 0 |
| prescreen-4000 | 921 | 0 |
| crawl-4500 | 348 | 0 |
| prescreen-4500 | 1555 | 0 |
| crawl-5000 | 3 | 1 |
| verify-default-20260729T155930Z | 10520 | 0 |
| verify-default-20260729T185453Z | 603 | 0 |
| verify-default-20260729T190457Z | 8 | 0 |
| requeue-resource-failures | 10 | 0 |
| verify-escalated-20260729T190516Z | 4306 | 0 |

## E2B task performance

| Repository | Language | Resources | Cold start (s) | Tests (s) | Peak MB | Task |
|---|---|---|---:|---:|---:|---|
| [NSPC911/rovr](https://github.com/NSPC911/rovr) | python | 1 CPU / 1024 MB | 0.42 | 37.47 | 308.3 | `tasks/alv-rovr-462fd8-e8002859-v2` |
| [zhnt/loushang](https://github.com/zhnt/loushang) | python | 1 CPU / 1024 MB | 0.63 | 67.07 | 196.3 | `tasks/alv-loushang-2b9ea9-7ed49fc9-v2` |
| [bitnami/sealed-secrets](https://github.com/bitnami/sealed-secrets) | go | 1 CPU / 1024 MB | 0.45 | 106.06 | 744.1 | `tasks/alv-sealed-secrets-2ab4a1-fb7da1e9-v2` |
| [hetznercloud/hcloud-cloud-controller-manager](https://github.com/hetznercloud/hcloud-cloud-controller-manager) | go | 1 CPU / 1024 MB | 0.48 | 91.86 | 665.8 | `tasks/alv-hcloud-cloud-control-a2a07e-27253f52-v2` |
| [kube-vip/kube-vip](https://github.com/kube-vip/kube-vip) | go | 1 CPU / 1024 MB | 0.39 | 27.91 | 144.5 | `tasks/alv-kube-vip-51d2e4-0d248ba4-v2` |
| [devswha/patina](https://github.com/devswha/patina) | javascript | 1 CPU / 1024 MB | 0.49 | 118.28 | 101.1 | `tasks/alv-patina-6b5b94-b98b3b03-v2` |
| [pgsty/pg_exporter](https://github.com/pgsty/pg_exporter) | go | 1 CPU / 1024 MB | 0.42 | 19.06 | 224.6 | `tasks/alv-pg-exporter-68d5bf-3fae4b01-v2` |
| [ClickHouse/clickhouse-go](https://github.com/ClickHouse/clickhouse-go) | go | 1 CPU / 1024 MB | 0.53 | 46.02 | 383.7 | `tasks/alv-clickhouse-go-6dd8a1-aee0e942-v2` |
| [cooperspencer/gickup](https://github.com/cooperspencer/gickup) | go | 1 CPU / 1024 MB | 0.59 | 39.04 | 440.9 | `tasks/alv-gickup-310952-66eaf7bd-v2` |
| [StuMason/coolify-mcp](https://github.com/StuMason/coolify-mcp) | typescript | 1 CPU / 1024 MB | 0.63 | 38.35 | 528.2 | `tasks/alv-coolify-mcp-cbb913-fcff9518-v2` |
| [grpc-ecosystem/grpc-gateway](https://github.com/grpc-ecosystem/grpc-gateway) | go | 1 CPU / 1024 MB | 0.47 | 13.55 | 179.1 | `tasks/alv-grpc-gateway-15b6ef-686c173f-v2` |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | go | 1 CPU / 1024 MB | 0.46 | 82.93 | 582.4 | `tasks/alv-github-mcp-server-ee5439-456fae9d-v2` |
| [TheManticoreProject/Manticore](https://github.com/TheManticoreProject/Manticore) | go | 1 CPU / 1024 MB | 0.41 | 89.96 | 230.2 | `tasks/alv-manticore-2870ab-68589c0a-v2` |
| [kmolan/multicalc-rust](https://github.com/kmolan/multicalc-rust) | rust | 1 CPU / 1024 MB | 0.37 | 9.73 | 157.2 | `tasks/alv-multicalc-rust-9f373b-54cfa52e-v2` |
| [uutils/sed](https://github.com/uutils/sed) | rust | 1 CPU / 1024 MB | 0.41 | 12.43 | 107.8 | `tasks/alv-sed-9b4d28-c7e1f784-v2` |
| [jackwener/OpenCLI](https://github.com/jackwener/OpenCLI) | javascript | 1 CPU / 1024 MB | 0.43 | 12.13 | 132.2 | `tasks/alv-opencli-d3f868-77812f0e-v2` |
| [rmyndharis/OpenWA](https://github.com/rmyndharis/OpenWA) | typescript | 1 CPU / 1024 MB | 0.49 | 119.05 | 580.7 | `tasks/alv-openwa-c2357e-20af3bdf-v2` |
| [open-telemetry/opentelemetry-go](https://github.com/open-telemetry/opentelemetry-go) | go | 1 CPU / 1024 MB | 0.51 | 38.3 | 155.8 | `tasks/alv-opentelemetry-go-6d0c33-2f4795fc-v2` |
| [suzuki-shunsuke/ghtkn](https://github.com/suzuki-shunsuke/ghtkn) | go | 1 CPU / 1024 MB | 0.58 | 25.82 | 181.9 | `tasks/alv-ghtkn-9d8b41-a7614658-v2` |
| [open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector) | go | 1 CPU / 1024 MB | 0.51 | 16.18 | 158.4 | `tasks/alv-opentelemetry-collec-525795-be178a74-v2` |
| [haproxytech/client-native](https://github.com/haproxytech/client-native) | go | 1 CPU / 1024 MB | 0.47 | 56.53 | 323.8 | `tasks/alv-client-native-aad6ca-0329e81c-v2` |
| [eslint-community/eslint-plugin-promise](https://github.com/eslint-community/eslint-plugin-promise) | javascript | 1 CPU / 1024 MB | 0.44 | 10.95 | 258.0 | `tasks/alv-eslint-plugin-promis-b52bd8-e34a0fa0-v2` |
| [oasdiff/oasdiff](https://github.com/oasdiff/oasdiff) | go | 1 CPU / 1024 MB | 0.51 | 37.35 | 251.4 | `tasks/alv-oasdiff-81085b-e5236e58-v2` |
| [eljulians/skillfile](https://github.com/eljulians/skillfile) | rust | 1 CPU / 1024 MB | 0.62 | 23.12 | 119.2 | `tasks/alv-skillfile-3ee39d-fd042844-v2` |
| [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | rust | 1 CPU / 1024 MB | 0.48 | 20.86 | 290.9 | `tasks/alv-ast-grep-14c759-115374d5-v2` |
| [a2aproject/a2a-go](https://github.com/a2aproject/a2a-go) | go | 1 CPU / 1024 MB | 0.54 | 38.13 | 240.0 | `tasks/alv-a2a-go-d98be9-3d5d8eb2-v2` |
| [se2p/pynguin](https://github.com/se2p/pynguin) | python | 1 CPU / 1024 MB | 0.6 | 97.49 | 278.5 | `tasks/alv-pynguin-6ff577-fa142caf-v2` |
| [hetznercloud/csi-driver](https://github.com/hetznercloud/csi-driver) | go | 1 CPU / 1024 MB | 0.56 | 49.07 | 319.2 | `tasks/alv-csi-driver-00079b-752f842e-v2` |
| [42wim/matterircd](https://github.com/42wim/matterircd) | go | 1 CPU / 1024 MB | 0.43 | 16.83 | 234.2 | `tasks/alv-matterircd-90ad2a-1af786ae-v2` |
| [quarylabs/sqruff](https://github.com/quarylabs/sqruff) | rust | 1 CPU / 1024 MB | 0.36 | 4.84 | 59.7 | `tasks/alv-sqruff-c986bf-55405940-v2` |
| [rust-lang/measureme](https://github.com/rust-lang/measureme) | rust | 1 CPU / 1024 MB | 0.43 | 11.25 | 532.4 | `tasks/alv-measureme-443bd6-e52be739-v2` |
| [alpha-omega-security/scrutineer](https://github.com/alpha-omega-security/scrutineer) | go | 1 CPU / 1024 MB | 0.53 | 100.05 | 800.6 | `tasks/alv-scrutineer-dcfefa-0b730829-v2` |
| [crossplane-contrib/provider-terraform](https://github.com/crossplane-contrib/provider-terraform) | go | 1 CPU / 1024 MB | 0.53 | 20.53 | 140.9 | `tasks/alv-provider-terraform-8957df-cde09999-v2` |
| [promhippie/github_exporter](https://github.com/promhippie/github_exporter) | go | 1 CPU / 1024 MB | 0.48 | 23.8 | 318.0 | `tasks/alv-github-exporter-86d4cf-7815e7a9-v2` |
| [Azure/azqr](https://github.com/Azure/azqr) | go | 1 CPU / 1024 MB | 0.59 | 43.77 | 299.5 | `tasks/alv-azqr-1e536e-ed6b9588-v2` |
| [rahilp/second-brain-cloudflare](https://github.com/rahilp/second-brain-cloudflare) | typescript | 1 CPU / 1024 MB | 0.47 | 24.84 | 174.0 | `tasks/alv-second-brain-cloudfl-7af7ed-371a8f98-v2` |
| [lima-vm/lima](https://github.com/lima-vm/lima) | go | 1 CPU / 1024 MB | 0.56 | 65.56 | 444.4 | `tasks/alv-lima-bb25e2-947c3caa-v2` |
| [salesforce/cloudsplaining](https://github.com/salesforce/cloudsplaining) | javascript | 1 CPU / 1024 MB | 0.49 | 2.54 | 71.6 | `tasks/alv-cloudsplaining-ec719d-a6f3c064-v2` |
| [redpanda-data/benthos](https://github.com/redpanda-data/benthos) | go | 1 CPU / 1024 MB | 0.4 | 13.54 | 115.6 | `tasks/alv-benthos-554aed-4ade611e-v2` |
| [nyx-space/hifitime](https://github.com/nyx-space/hifitime) | rust | 1 CPU / 1024 MB | 0.46 | 9.74 | 105.8 | `tasks/alv-hifitime-1e9ac1-7b6238d0-v2` |
| [interlink-hq/interLink](https://github.com/interlink-hq/interLink) | go | 1 CPU / 1024 MB | 0.47 | 107.04 | 728.7 | `tasks/alv-interlink-299fa4-77b31b71-v2` |
| [quinn-rs/quinn](https://github.com/quinn-rs/quinn) | rust | 1 CPU / 1024 MB | 0.52 | 30.97 | 416.6 | `tasks/alv-quinn-4679cd-ba294586-v2` |
| [plabayo/rama](https://github.com/plabayo/rama) | rust | 1 CPU / 1024 MB | 0.47 | 5.53 | 87.3 | `tasks/alv-rama-c20868-89bf2b36-v2` |
| [rudof-project/rudof](https://github.com/rudof-project/rudof) | rust | 1 CPU / 1024 MB | 0.55 | 9.02 | 170.2 | `tasks/alv-rudof-03fbed-b18be6da-v2` |
| [apache/opendal-reqsign](https://github.com/apache/opendal-reqsign) | rust | 1 CPU / 1024 MB | 0.84 | 82.04 | 518.3 | `tasks/alv-opendal-reqsign-06eb54-79e2ba6f-v2` |
| [mooman219/fontdue](https://github.com/mooman219/fontdue) | rust | 1 CPU / 1024 MB | 0.41 | 5.3 | 162.2 | `tasks/alv-fontdue-2c0a13-2924772f-v2` |
| [MarketSquare/robotframework-robocop](https://github.com/MarketSquare/robotframework-robocop) | python | 1 CPU / 1024 MB | 0.56 | 35.98 | 207.9 | `tasks/alv-robotframework-roboc-01a60f-1a3147fe-v2` |
| [phires/go-guerrilla](https://github.com/phires/go-guerrilla) | go | 1 CPU / 1024 MB | 0.64 | 75.19 | 174.0 | `tasks/alv-go-guerrilla-0a19f8-e6f6738e-v2` |
| [google/go-containerregistry](https://github.com/google/go-containerregistry) | go | 1 CPU / 1024 MB | 0.58 | 63.16 | 213.5 | `tasks/alv-go-containerregistry-13a8c1-fb196956-v2` |
| [kdl-org/kdl-rs](https://github.com/kdl-org/kdl-rs) | rust | 1 CPU / 1024 MB | 0.41 | 7.98 | 153.8 | `tasks/alv-kdl-rs-fa942e-bf1a12dd-v2` |
| [linode/terraform-provider-linode](https://github.com/linode/terraform-provider-linode) | go | 1 CPU / 1024 MB | 0.58 | 58.19 | 145.7 | `tasks/alv-terraform-provider-l-b6b47e-ef6379f0-v2` |
| [CircleCI-Public/circleci-cli](https://github.com/CircleCI-Public/circleci-cli) | go | 1 CPU / 1024 MB | 0.42 | 68.44 | 517.3 | `tasks/alv-circleci-cli-ad34fc-b726fcdd-v2` |
| [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) | go | 1 CPU / 1024 MB | 0.53 | 118.98 | 745.2 | `tasks/alv-mcp-grafana-984281-1071e4f1-v2` |
| [stackrox/kube-linter](https://github.com/stackrox/kube-linter) | go | 1 CPU / 1024 MB | 0.53 | 59.32 | 749.3 | `tasks/alv-kube-linter-df4e9b-75b6ee58-v2` |
| [CrowdStrike/falcon-mcp](https://github.com/CrowdStrike/falcon-mcp) | python | 1 CPU / 1024 MB | 0.44 | 11.74 | 108.3 | `tasks/alv-falcon-mcp-6e4d09-ab97afde-v2` |
| [Javis603/token-monitor](https://github.com/Javis603/token-monitor) | javascript | 1 CPU / 1024 MB | 0.52 | 28.78 | 89.3 | `tasks/alv-token-monitor-389c50-515a0142-v2` |
| [vouchdev/vouch](https://github.com/vouchdev/vouch) | python | 1 CPU / 1024 MB | 0.48 | 61.17 | 122.5 | `tasks/alv-vouch-238f07-302363ca-v2` |
| [junegunn/fzf](https://github.com/junegunn/fzf) | go | 1 CPU / 1024 MB | 0.58 | 21.54 | 233.2 | `tasks/alv-fzf-aefedf-b6615382-v2` |
| [open-telemetry/opentelemetry-go-contrib](https://github.com/open-telemetry/opentelemetry-go-contrib) | go | 1 CPU / 1024 MB | 0.56 | 38.59 | 237.1 | `tasks/alv-opentelemetry-go-con-270801-e3dc9d9d-v2` |
| [raviqqe/muffet](https://github.com/raviqqe/muffet) | go | 1 CPU / 1024 MB | 0.53 | 16.22 | 181.3 | `tasks/alv-muffet-a3d0b2-d23fa291-v2` |
| [rancher/local-path-provisioner](https://github.com/rancher/local-path-provisioner) | go | 1 CPU / 1024 MB | 0.53 | 60.23 | 695.8 | `tasks/alv-local-path-provision-48a860-62e0594d-v2` |
| [googlefonts/fontations](https://github.com/googlefonts/fontations) | rust | 1 CPU / 1024 MB | 0.44 | 30.93 | 278.6 | `tasks/alv-fontations-f03436-7255a6a7-v2` |
| [Spenhouet/confluence-markdown-exporter](https://github.com/Spenhouet/confluence-markdown-exporter) | python | 1 CPU / 1024 MB | 0.61 | 44.18 | 83.7 | `tasks/alv-confluence-markdown--41a1bd-79c9289d-v2` |
| [flohoss/gocron](https://github.com/flohoss/gocron) | go | 1 CPU / 1024 MB | 0.44 | 30.9 | 800.5 | `tasks/alv-gocron-0b005b-a63867c1-v2` |
| [pmady/keda-gpu-scaler](https://github.com/pmady/keda-gpu-scaler) | go | 1 CPU / 1024 MB | 0.43 | 28.72 | 217.1 | `tasks/alv-keda-gpu-scaler-5f608f-c1e7daac-v2` |
| [agentrhq/webcmd](https://github.com/agentrhq/webcmd) | javascript | 1 CPU / 1024 MB | 0.4 | 58.23 | 182.7 | `tasks/alv-webcmd-1df241-6c439f85-v2` |
| [fossasia/voxbento](https://github.com/fossasia/voxbento) | python | 2 CPU / 4096 MB | 0.56 | 30.97 | 155.2 | `tasks/alv-voxbento-0c7806-0d3d06c9-v2` |
| [danielgtaylor/huma](https://github.com/danielgtaylor/huma) | go | 2 CPU / 4096 MB | 0.52 | 27.21 | 584.7 | `tasks/alv-huma-17c347-198225ea-v2` |
| [attestantio/go-eth2-client](https://github.com/attestantio/go-eth2-client) | go | 2 CPU / 4096 MB | 0.45 | 34.21 | 1091.1 | `tasks/alv-go-eth2-client-dff3f9-85ac0f6e-v2` |
| [Annoraaq/grid-engine](https://github.com/Annoraaq/grid-engine) | typescript | 2 CPU / 4096 MB | 0.55 | 37.65 | 1293.9 | `tasks/alv-grid-engine-64e008-aeb156ed-v2` |
| [epam/ai-dial-chat](https://github.com/epam/ai-dial-chat) | typescript | 2 CPU / 4096 MB | 0.47 | 92.37 | 420.0 | `tasks/alv-ai-dial-chat-bc1bf2-3c644131-v2` |
| [algesten/str0m](https://github.com/algesten/str0m) | rust | 2 CPU / 4096 MB | 0.52 | 100.68 | 758.6 | `tasks/alv-str0m-290754-d7368c85-v2` |
| [tektoncd/pipelines-as-code](https://github.com/tektoncd/pipelines-as-code) | go | 2 CPU / 4096 MB | 0.47 | 6.37 | 154.5 | `tasks/alv-pipelines-as-code-2d6fb9-e309d1a6-v2` |
| [terraform-provider-openstack/terraform-provider-openstack](https://github.com/terraform-provider-openstack/terraform-provider-openstack) | go | 2 CPU / 4096 MB | 0.56 | 33.03 | 1030.5 | `tasks/alv-terraform-provider-o-c95f38-0fbdf8f8-v2` |
| [crossplane-contrib/provider-helm](https://github.com/crossplane-contrib/provider-helm) | go | 2 CPU / 4096 MB | 0.43 | 59.47 | 1148.0 | `tasks/alv-provider-helm-7cc9b5-122e0ce1-v2` |
| [ENTERPILOT/GoModel](https://github.com/ENTERPILOT/GoModel) | go | 2 CPU / 4096 MB | 0.54 | 110.54 | 768.8 | `tasks/alv-gomodel-bf3f5d-cdad1458-v2` |
| [ratel-ai/ratel](https://github.com/ratel-ai/ratel) | rust | 2 CPU / 4096 MB | 0.58 | 35.95 | 899.1 | `tasks/alv-ratel-e95925-caa4bf6f-v2` |
| [openyida/openyida](https://github.com/openyida/openyida) | javascript | 2 CPU / 4096 MB | 0.54 | 109.67 | 1799.3 | `tasks/alv-openyida-23208f-68b772d1-v2` |
| [uber-go/nilaway](https://github.com/uber-go/nilaway) | go | 2 CPU / 4096 MB | 0.41 | 55.14 | 1880.5 | `tasks/alv-nilaway-e546d3-c82f9684-v2` |
| [buildkite/lifecycled](https://github.com/buildkite/lifecycled) | go | 2 CPU / 4096 MB | 0.6 | 16.31 | 1140.6 | `tasks/alv-lifecycled-4c85f1-0a944f09-v2` |
| [VirusTotal/yara-x](https://github.com/VirusTotal/yara-x) | rust | 2 CPU / 4096 MB | 0.43 | 100.84 | 1702.3 | `tasks/alv-yara-x-acf45d-832603bb-v2` |
| [amikos-tech/chroma-go](https://github.com/amikos-tech/chroma-go) | go | 2 CPU / 4096 MB | 0.63 | 23.96 | 998.1 | `tasks/alv-chroma-go-deaf6e-d475ee2c-v2` |
| [abdolence/slack-morphism-rust](https://github.com/abdolence/slack-morphism-rust) | rust | 2 CPU / 4096 MB | 0.5 | 24.35 | 838.5 | `tasks/alv-slack-morphism-rust-a12632-65482925-v2` |
| [dmtrKovalenko/fff](https://github.com/dmtrKovalenko/fff) | rust | 2 CPU / 4096 MB | 0.54 | 49.71 | 630.0 | `tasks/alv-fff-64a975-2cf87121-v2` |
| [openziti/ziti](https://github.com/openziti/ziti) | go | 2 CPU / 4096 MB | 0.43 | 21.1 | 178.0 | `tasks/alv-ziti-1cf805-465b34d3-v2` |
| [ferronweb/ferron](https://github.com/ferronweb/ferron) | rust | 2 CPU / 4096 MB | 0.47 | 34.46 | 2156.4 | `tasks/alv-ferron-f40dc5-8d2e31d1-v2` |
| [k8sgpt-ai/k8sgpt](https://github.com/k8sgpt-ai/k8sgpt) | go | 2 CPU / 4096 MB | 0.39 | 71.87 | 1711.5 | `tasks/alv-k8sgpt-e85776-3cf40988-v2` |

## Logs

Raw stage logs are under `outputs/production-runs/github-mass-production-XBY-20260729/logs`.
