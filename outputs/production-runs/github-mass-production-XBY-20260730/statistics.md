# Pipeline statistics: github-mass-production-XBY-20260730

- Status: `complete`
- Generated: `2026-07-30T10:30:05.198355+00:00`
- Raw GitHub sample: 10000
- Initial filter accepted: 5027
- E2B queue: 1275
- Deliverable tasks: 286
- Pending: 0

## Language funnel

| Language | Initial accepted | Final tasks |
|---|---:|---:|
| python | 1025 | 35 |
| go | 1428 | 127 |
| typescript | 819 | 21 |
| javascript | 563 | 26 |
| rust | 1192 | 77 |

## Stage timings

| Stage | Duration (s) | Exit |
|---|---:|---:|
| prescreen-resume-4500 | 2 | 0 |
| crawl-5000 | 334 | 0 |
| prescreen-5000 | 778 | 0 |
| crawl-5500 | 328 | 0 |
| prescreen-5500 | 1646 | 0 |
| crawl-6000 | 230 | 130 |
| prescreen-resume-5500 | 634 | 0 |
| crawl-6000 | 98 | 0 |
| prescreen-6000 | 352 | 0 |
| crawl-6500 | 332 | 0 |
| prescreen-6500 | 602 | 0 |
| crawl-7000 | 309 | 0 |
| prescreen-7000 | 770 | 0 |
| crawl-7500 | 2121 | 0 |
| prescreen-7500 | 705 | 0 |
| crawl-8000 | 326 | 0 |
| prescreen-8000 | 952 | 0 |
| crawl-8500 | 195 | 130 |
| repair-rebuildable-packages | 2 | 0 |
| prescreen-resume-8000 | 395 | 0 |
| crawl-8500 | 183 | 0 |
| prescreen-8500 | 352 | 0 |
| crawl-9000 | 361 | 0 |
| prescreen-9000 | 783 | 0 |
| crawl-9500 | 154 | 130 |
| repair-rebuildable-packages | 3 | 0 |
| prescreen-resume-9000 | 548 | 0 |
| crawl-9500 | 212 | 0 |
| prescreen-9500 | 1063 | 0 |
| crawl-10000 | 352 | 0 |
| prescreen-10000 | 1716 | 0 |
| verify-default-20260730T073838Z | 4343 | 0 |
| verify-default-20260730T085106Z | 3 | 2 |
| repair-rebuildable-packages | 3 | 0 |
| prescreen-resume-10000 | 3 | 0 |
| verify-default-20260730T091621Z | 16 | 0 |
| verify-default-20260730T091653Z | 20 | 0 |
| requeue-resource-failures | 42 | 0 |
| verify-escalated-20260730T091757Z | 4322 | 0 |

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
| [ota-meshi/eslint-plugin-regexp](https://github.com/ota-meshi/eslint-plugin-regexp) | typescript | 1 CPU / 1024 MB | 0.41 | 32.9 | 543.9 | `tasks/alv-eslint-plugin-regexp-f86dc5-ffee3bc9-v2` |
| [Luzifer/nginx-sso](https://github.com/Luzifer/nginx-sso) | go | 1 CPU / 1024 MB | 0.45 | 25.12 | 312.4 | `tasks/alv-nginx-sso-c311c7-499f0129-v2` |
| [ergochat/ergo](https://github.com/ergochat/ergo) | go | 1 CPU / 1024 MB | 0.52 | 29.06 | 240.3 | `tasks/alv-ergo-5ae04f-65875b7c-v2` |
| [pulldown-cmark/pulldown-cmark](https://github.com/pulldown-cmark/pulldown-cmark) | rust | 1 CPU / 1024 MB | 0.51 | 10.15 | 147.6 | `tasks/alv-pulldown-cmark-606fbb-7a00f309-v2` |
| [python-hyper/h2](https://github.com/python-hyper/h2) | python | 1 CPU / 1024 MB | 0.51 | 13.15 | 217.8 | `tasks/alv-h2-7e93b0-04d3b87c-v2` |
| [TIGER-AI-Lab/ClawBench](https://github.com/TIGER-AI-Lab/ClawBench) | python | 1 CPU / 1024 MB | 0.49 | 5.54 | 76.7 | `tasks/alv-clawbench-e34f0f-86fdd307-v2` |
| [schapman1974/tinymongo](https://github.com/schapman1974/tinymongo) | python | 1 CPU / 1024 MB | 0.53 | 39.67 | 164.1 | `tasks/alv-tinymongo-991055-a7d53044-v2` |
| [imroc/req](https://github.com/imroc/req) | go | 1 CPU / 1024 MB | 0.54 | 32.28 | 209.8 | `tasks/alv-req-ba3c6e-d34ebe52-v2` |
| [ShunmeiCho/cc-clip](https://github.com/ShunmeiCho/cc-clip) | go | 1 CPU / 1024 MB | 0.5 | 22.18 | 153.1 | `tasks/alv-cc-clip-ac0517-becdae87-v2` |
| [mathworks/MATLAB-language-server](https://github.com/mathworks/MATLAB-language-server) | typescript | 1 CPU / 1024 MB | 0.54 | 5.07 | 134.2 | `tasks/alv-matlab-language-serv-12cccd-3997ef66-v2` |
| [bfirsh/jsnes](https://github.com/bfirsh/jsnes) | javascript | 1 CPU / 1024 MB | 0.53 | 17.76 | 133.1 | `tasks/alv-jsnes-9ac844-b8a45d08-v2` |
| [easyp-tech/easyp](https://github.com/easyp-tech/easyp) | go | 1 CPU / 1024 MB | 0.43 | 33.38 | 286.0 | `tasks/alv-easyp-4aa7c8-78168591-v2` |
| [grafana/cog](https://github.com/grafana/cog) | go | 1 CPU / 1024 MB | 0.51 | 43.53 | 374.8 | `tasks/alv-cog-9f8897-9e62719b-v2` |
| [fsouza/fake-gcs-server](https://github.com/fsouza/fake-gcs-server) | go | 1 CPU / 1024 MB | 0.55 | 60.47 | 551.0 | `tasks/alv-fake-gcs-server-0a60c2-676ce4ba-v2` |
| [algolia/cli](https://github.com/algolia/cli) | go | 1 CPU / 1024 MB | 0.5 | 82.31 | 320.6 | `tasks/alv-cli-0c2f6d-8657322d-v2` |
| [NVIDIA/k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin) | go | 1 CPU / 1024 MB | 0.56 | 92.76 | 674.5 | `tasks/alv-k8s-device-plugin-c09e18-5f27eeee-v2` |
| [crossplane/upjet](https://github.com/crossplane/upjet) | go | 1 CPU / 1024 MB | 0.46 | 71.08 | 727.1 | `tasks/alv-upjet-e42f5f-4f6e6e10-v2` |
| [hoodie/icalendar](https://github.com/hoodie/icalendar) | rust | 1 CPU / 1024 MB | 0.51 | 11.33 | 127.5 | `tasks/alv-icalendar-4a45eb-27d4f11b-v2` |
| [microsoft/python-environment-tools](https://github.com/microsoft/python-environment-tools) | rust | 1 CPU / 1024 MB | 0.47 | 12.09 | 148.5 | `tasks/alv-python-environment-t-742fea-b6181976-v2` |
| [rstcheck/rstcheck](https://github.com/rstcheck/rstcheck) | python | 1 CPU / 1024 MB | 0.46 | 7.79 | 86.6 | `tasks/alv-rstcheck-2d6d59-d8774e96-v2` |
| [mirumee/ariadne-codegen](https://github.com/mirumee/ariadne-codegen) | python | 1 CPU / 1024 MB | 0.51 | 11.18 | 85.9 | `tasks/alv-ariadne-codegen-11c5b0-083d1802-v2` |
| [hashicorp/go-bexpr](https://github.com/hashicorp/go-bexpr) | go | 1 CPU / 1024 MB | 0.54 | 23.73 | 181.7 | `tasks/alv-go-bexpr-42908c-667dc3de-v2` |
| [ByteNess/aws-vault](https://github.com/ByteNess/aws-vault) | go | 1 CPU / 1024 MB | 0.68 | 28.27 | 359.9 | `tasks/alv-aws-vault-152aa8-7d03fd26-v2` |
| [marp-team/marp-core](https://github.com/marp-team/marp-core) | typescript | 1 CPU / 1024 MB | 0.48 | 25.74 | 273.6 | `tasks/alv-marp-core-548b21-fb41436e-v2` |
| [allen-cell-animated/vole-core](https://github.com/allen-cell-animated/vole-core) | typescript | 1 CPU / 1024 MB | 0.53 | 11.58 | 156.0 | `tasks/alv-vole-core-0375b0-5f324f70-v2` |
| [microsoft/RAMPART](https://github.com/microsoft/RAMPART) | python | 1 CPU / 1024 MB | 0.62 | 87.42 | 346.6 | `tasks/alv-rampart-f33e18-64754221-v2` |
| [betterleaks/betterleaks](https://github.com/betterleaks/betterleaks) | go | 1 CPU / 1024 MB | 0.48 | 36.8 | 302.4 | `tasks/alv-betterleaks-c639e2-b9de7fd8-v2` |
| [containerd/accelerated-container-image](https://github.com/containerd/accelerated-container-image) | go | 1 CPU / 1024 MB | 0.59 | 32.36 | 282.7 | `tasks/alv-accelerated-containe-81fa2d-b00987e1-v2` |
| [nbelyh/editsvgcode](https://github.com/nbelyh/editsvgcode) | javascript | 1 CPU / 1024 MB | 0.37 | 14.73 | 170.7 | `tasks/alv-editsvgcode-9ddc38-f04bbb03-v2` |
| [nodejs/node-core-utils](https://github.com/nodejs/node-core-utils) | javascript | 1 CPU / 1024 MB | 0.49 | 22.68 | 209.1 | `tasks/alv-node-core-utils-8ffc60-828f4277-v2` |
| [eugenioenko/ttt](https://github.com/eugenioenko/ttt) | go | 1 CPU / 1024 MB | 0.49 | 92.66 | 205.9 | `tasks/alv-ttt-b62de1-f14334f0-v2` |
| [Project-OSRM/osrm-text-instructions](https://github.com/Project-OSRM/osrm-text-instructions) | javascript | 1 CPU / 1024 MB | 0.59 | 16.78 | 86.1 | `tasks/alv-osrm-text-instructio-7757cf-c60c3bd0-v2` |
| [maxfield-allison/dnsweaver](https://github.com/maxfield-allison/dnsweaver) | go | 1 CPU / 1024 MB | 0.5 | 87.63 | 217.9 | `tasks/alv-dnsweaver-e359fd-316ba942-v2` |
| [k8up-io/k8up](https://github.com/k8up-io/k8up) | go | 1 CPU / 1024 MB | 0.51 | 91.18 | 721.2 | `tasks/alv-k8up-8f5dc1-55b207dd-v2` |
| [aquasecurity/kube-bench](https://github.com/aquasecurity/kube-bench) | go | 1 CPU / 1024 MB | 0.5 | 55.78 | 748.2 | `tasks/alv-kube-bench-e65b9f-2dc17e77-v2` |
| [aws/aws-lambda-web-adapter](https://github.com/aws/aws-lambda-web-adapter) | rust | 1 CPU / 1024 MB | 0.57 | 13.32 | 360.6 | `tasks/alv-aws-lambda-web-adapt-9ca7a5-34d3a299-v2` |
| [smartcorelib/smartcore](https://github.com/smartcorelib/smartcore) | rust | 1 CPU / 1024 MB | 0.61 | 88.12 | 468.6 | `tasks/alv-smartcore-54886c-3febb4ce-v2` |
| [dfinity/candid](https://github.com/dfinity/candid) | rust | 1 CPU / 1024 MB | 0.52 | 16.45 | 299.8 | `tasks/alv-candid-9017e3-b8c17d34-v2` |
| [ynqa/promkit](https://github.com/ynqa/promkit) | rust | 1 CPU / 1024 MB | 0.58 | 86.02 | 434.4 | `tasks/alv-promkit-91dd76-ba80ea21-v2` |
| [Andyyyy64/whichllm](https://github.com/Andyyyy64/whichllm) | python | 1 CPU / 1024 MB | 0.41 | 3.56 | 79.3 | `tasks/alv-whichllm-6f0f23-0a49590d-v2` |
| [pycontribs/mk](https://github.com/pycontribs/mk) | python | 1 CPU / 1024 MB | 0.5 | 4.43 | 45.7 | `tasks/alv-mk-69a136-db4de3f4-v2` |
| [astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone) | python | 1 CPU / 1024 MB | 0.44 | 3.76 | 117.0 | `tasks/alv-python-build-standal-f9fd07-c1991f8f-v2` |
| [VictoriaMetrics/metrics](https://github.com/VictoriaMetrics/metrics) | go | 1 CPU / 1024 MB | 0.4 | 12.35 | 137.5 | `tasks/alv-metrics-98314a-ca1b05d1-v2` |
| [antonmedv/fx](https://github.com/antonmedv/fx) | go | 1 CPU / 1024 MB | 0.52 | 35.19 | 270.9 | `tasks/alv-fx-4bb5a6-63eb255a-v2` |
| [H4ad/serverless-adapter](https://github.com/H4ad/serverless-adapter) | typescript | 1 CPU / 1024 MB | 0.47 | 31.8 | 133.1 | `tasks/alv-serverless-adapter-24caf7-a44e1077-v2` |
| [funbiscuit/embedded-cli-rs](https://github.com/funbiscuit/embedded-cli-rs) | rust | 1 CPU / 1024 MB | 0.49 | 4.14 | 90.0 | `tasks/alv-embedded-cli-rs-2794f4-1ce2a857-v2` |
| [NLnetLabs/domain](https://github.com/NLnetLabs/domain) | rust | 1 CPU / 1024 MB | 0.42 | 7.82 | 179.4 | `tasks/alv-domain-17d70b-fa52d81a-v2` |
| [coreos/bootupd](https://github.com/coreos/bootupd) | rust | 1 CPU / 1024 MB | 0.44 | 1.99 | 52.0 | `tasks/alv-bootupd-17c0d3-8f5cc497-v2` |
| [losisin/helm-values-schema-json](https://github.com/losisin/helm-values-schema-json) | go | 1 CPU / 1024 MB | 0.43 | 14.83 | 180.5 | `tasks/alv-helm-values-schema-j-b197e0-27dfb7fa-v2` |
| [ActivityWatch/aw-server-rust](https://github.com/ActivityWatch/aw-server-rust) | rust | 1 CPU / 1024 MB | 0.66 | 21.52 | 478.2 | `tasks/alv-aw-server-rust-de5763-45ca2936-v2` |
| [agsh/onvif](https://github.com/agsh/onvif) | javascript | 1 CPU / 1024 MB | 0.5 | 23.23 | 110.9 | `tasks/alv-onvif-3047d8-151f9647-v2` |
| [Thriftpy/thriftpy2](https://github.com/Thriftpy/thriftpy2) | python | 1 CPU / 1024 MB | 0.58 | 47.46 | 77.4 | `tasks/alv-thriftpy2-10ab0c-29e05a21-v2` |
| [x1unix/go-playground](https://github.com/x1unix/go-playground) | go | 1 CPU / 1024 MB | 0.62 | 22.59 | 155.8 | `tasks/alv-go-playground-e9ae11-cb3526af-v2` |
| [offen/docker-volume-backup](https://github.com/offen/docker-volume-backup) | go | 1 CPU / 1024 MB | 0.61 | 31.45 | 413.5 | `tasks/alv-docker-volume-backup-2f5b49-bc09f80f-v2` |
| [vrc-get/vrc-get](https://github.com/vrc-get/vrc-get) | rust | 1 CPU / 1024 MB | 0.46 | 7.26 | 157.0 | `tasks/alv-vrc-get-dd0c4f-52eb97ed-v2` |
| [apache/avro-rs](https://github.com/apache/avro-rs) | rust | 1 CPU / 1024 MB | 0.48 | 25.35 | 196.4 | `tasks/alv-avro-rs-353b5f-006ac897-v2` |
| [open-ug/conveyor](https://github.com/open-ug/conveyor) | go | 1 CPU / 1024 MB | 0.4 | 51.82 | 592.1 | `tasks/alv-conveyor-0c9fa2-aeaf5d98-v2` |
| [sigstore/rekor](https://github.com/sigstore/rekor) | go | 1 CPU / 1024 MB | 0.38 | 54.42 | 725.7 | `tasks/alv-rekor-ce1847-f3299aac-v2` |
| [crossplane-contrib/provider-sql](https://github.com/crossplane-contrib/provider-sql) | go | 1 CPU / 1024 MB | 0.45 | 57.74 | 706.8 | `tasks/alv-provider-sql-8bbcb3-985277d9-v2` |
| [ReactiveX/RxPY](https://github.com/ReactiveX/RxPY) | python | 1 CPU / 1024 MB | 0.53 | 23.24 | 67.9 | `tasks/alv-rxpy-52140e-50e613bc-v2` |
| [elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp) | python | 1 CPU / 1024 MB | 0.63 | 4.21 | 88.4 | `tasks/alv-elevenlabs-mcp-9dc48b-a9426ee2-v2` |
| [Shopify/toxiproxy](https://github.com/Shopify/toxiproxy) | go | 1 CPU / 1024 MB | 0.49 | 24.11 | 164.8 | `tasks/alv-toxiproxy-893087-94d6d4b3-v2` |
| [noborus/ov](https://github.com/noborus/ov) | go | 1 CPU / 1024 MB | 0.48 | 22.9 | 538.2 | `tasks/alv-ov-f5b709-f7f8fbc2-v2` |
| [SolidOS/solid-panes](https://github.com/SolidOS/solid-panes) | javascript | 1 CPU / 1024 MB | 0.52 | 9.09 | 231.3 | `tasks/alv-solid-panes-540a94-2e3f100a-v2` |
| [mixpanel/mixpanel-js](https://github.com/mixpanel/mixpanel-js) | javascript | 1 CPU / 1024 MB | 0.46 | 18.13 | 270.1 | `tasks/alv-mixpanel-js-d52b9b-a8f8c363-v2` |
| [rust-cross/cargo-zigbuild](https://github.com/rust-cross/cargo-zigbuild) | rust | 1 CPU / 1024 MB | 0.4 | 4.49 | 103.6 | `tasks/alv-cargo-zigbuild-4a8cac-0d2d958f-v2` |
| [J0R6IT0/navidrome-lyrics-plugin](https://github.com/J0R6IT0/navidrome-lyrics-plugin) | rust | 1 CPU / 1024 MB | 0.41 | 1.24 | 35.1 | `tasks/alv-navidrome-lyrics-plu-f72dbc-e940b1dc-v2` |
| [kewisch/ical.js](https://github.com/kewisch/ical.js) | javascript | 1 CPU / 1024 MB | 0.41 | 6.07 | 94.9 | `tasks/alv-ical-js-cefd21-cd2ef47d-v2` |
| [whawker/react-jsx-highcharts](https://github.com/whawker/react-jsx-highcharts) | javascript | 1 CPU / 1024 MB | 0.48 | 37.95 | 456.2 | `tasks/alv-react-jsx-highcharts-a8b447-aacf810e-v2` |
| [nutthouse/tutti](https://github.com/nutthouse/tutti) | rust | 1 CPU / 1024 MB | 0.57 | 8.52 | 83.9 | `tasks/alv-tutti-2221cf-6b86cca7-v2` |
| [Azure/secrets-store-csi-driver-provider-azure](https://github.com/Azure/secrets-store-csi-driver-provider-azure) | go | 1 CPU / 1024 MB | 0.54 | 117.39 | 355.6 | `tasks/alv-secrets-store-csi-dr-5e60c7-d5f7cf5b-v2` |
| [mbhall88/rasusa](https://github.com/mbhall88/rasusa) | rust | 1 CPU / 1024 MB | 0.47 | 96.61 | 343.1 | `tasks/alv-rasusa-1106d3-1d8a9830-v2` |
| [caddyserver/ingress](https://github.com/caddyserver/ingress) | go | 1 CPU / 1024 MB | 0.63 | 108.14 | 728.3 | `tasks/alv-ingress-32c899-0e3de1ed-v2` |
| [etcd-io/raft](https://github.com/etcd-io/raft) | go | 1 CPU / 1024 MB | 0.51 | 19.37 | 167.8 | `tasks/alv-raft-dca5cb-56e32004-v2` |
| [DopplerHQ/cli](https://github.com/DopplerHQ/cli) | go | 1 CPU / 1024 MB | 0.56 | 17.58 | 178.2 | `tasks/alv-cli-862609-d441d94d-v2` |
| [gokcehan/lf](https://github.com/gokcehan/lf) | go | 1 CPU / 1024 MB | 0.47 | 10.81 | 164.8 | `tasks/alv-lf-d1df38-fb668f12-v2` |
| [interlynk-io/sbomqs](https://github.com/interlynk-io/sbomqs) | go | 1 CPU / 1024 MB | 0.35 | 55.02 | 218.2 | `tasks/alv-sbomqs-442999-dec3e3ca-v2` |
| [cashapp/hermit](https://github.com/cashapp/hermit) | go | 1 CPU / 1024 MB | 0.52 | 29.83 | 233.7 | `tasks/alv-hermit-ce7852-449e375a-v2` |
| [cdimascio/express-openapi-validator](https://github.com/cdimascio/express-openapi-validator) | typescript | 1 CPU / 1024 MB | 0.47 | 45.95 | 326.3 | `tasks/alv-express-openapi-vali-f35cd4-03f11113-v2` |
| [Tantalor93/dnspyre](https://github.com/Tantalor93/dnspyre) | go | 1 CPU / 1024 MB | 0.5 | 73.56 | 303.5 | `tasks/alv-dnspyre-80fbd5-88d3599d-v2` |
| [1Password/shell-plugins](https://github.com/1Password/shell-plugins) | go | 1 CPU / 1024 MB | 0.48 | 42.61 | 224.1 | `tasks/alv-shell-plugins-387e64-fec9cd00-v2` |
| [encodeous/nylon](https://github.com/encodeous/nylon) | go | 1 CPU / 1024 MB | 0.55 | 32.67 | 224.2 | `tasks/alv-nylon-3b0942-a52885cd-v2` |
| [rust-vmm/vhost](https://github.com/rust-vmm/vhost) | rust | 1 CPU / 1024 MB | 0.48 | 4.42 | 105.7 | `tasks/alv-vhost-936359-a6c388db-v2` |
| [lucaslorentz/caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy) | go | 1 CPU / 1024 MB | 0.5 | 62.41 | 750.9 | `tasks/alv-caddy-docker-proxy-dcb6fa-d246679c-v2` |
| [readmeio/api](https://github.com/readmeio/api) | typescript | 1 CPU / 1024 MB | 0.54 | 89.96 | 551.6 | `tasks/alv-api-bf46a5-80166c44-v2` |
| [aws/aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator) | go | 1 CPU / 1024 MB | 0.53 | 50.91 | 170.9 | `tasks/alv-aws-lambda-runtime-i-852a5f-a0f264ae-v2` |
| [freedesktop-rs/nmrs](https://github.com/freedesktop-rs/nmrs) | rust | 1 CPU / 1024 MB | 0.6 | 32.26 | 354.8 | `tasks/alv-nmrs-c24d93-c51da7d4-v2` |
| [databus23/helm-diff](https://github.com/databus23/helm-diff) | go | 1 CPU / 1024 MB | 0.43 | 80.1 | 756.6 | `tasks/alv-helm-diff-882f82-01d88c2a-v2` |
| [ErsatzTV/next](https://github.com/ErsatzTV/next) | rust | 1 CPU / 1024 MB | 0.47 | 7.41 | 133.5 | `tasks/alv-next-3d3ae6-efd7aa67-v2` |
| [uber/kraken](https://github.com/uber/kraken) | go | 1 CPU / 1024 MB | 0.42 | 28.99 | 247.0 | `tasks/alv-kraken-8ba169-a4732524-v2` |
| [opendatalab/labelU](https://github.com/opendatalab/labelU) | python | 1 CPU / 1024 MB | 0.57 | 11.7 | 150.1 | `tasks/alv-labelu-94cd19-8681ca49-v2` |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | python | 1 CPU / 1024 MB | 0.56 | 13.11 | 65.1 | `tasks/alv-ida-pro-mcp-1f166b-80d7d36a-v2` |
| [pydata/bottleneck](https://github.com/pydata/bottleneck) | python | 1 CPU / 1024 MB | 0.45 | 28.17 | 57.8 | `tasks/alv-bottleneck-02c634-a088d385-v2` |
| [Farama-Foundation/HighwayEnv](https://github.com/Farama-Foundation/HighwayEnv) | python | 1 CPU / 1024 MB | 0.65 | 41.28 | 172.6 | `tasks/alv-highwayenv-d57041-cd1242c7-v2` |
| [supakeen/pinnwand](https://github.com/supakeen/pinnwand) | python | 1 CPU / 1024 MB | 0.55 | 22.05 | 115.4 | `tasks/alv-pinnwand-d8e072-c779e8fd-v2` |
| [golang/geo](https://github.com/golang/geo) | go | 1 CPU / 1024 MB | 0.56 | 20.22 | 308.2 | `tasks/alv-geo-e02703-857a528a-v2` |
| [maxlerebourg/crowdsec-bouncer-traefik-plugin](https://github.com/maxlerebourg/crowdsec-bouncer-traefik-plugin) | go | 1 CPU / 1024 MB | 0.38 | 9.86 | 124.5 | `tasks/alv-crowdsec-bouncer-tra-5327c1-ed4a9e82-v2` |
| [goreleaser/nfpm](https://github.com/goreleaser/nfpm) | go | 1 CPU / 1024 MB | 0.44 | 68.68 | 272.4 | `tasks/alv-nfpm-ba67be-f8299ae3-v2` |
| [homeport/havener](https://github.com/homeport/havener) | go | 1 CPU / 1024 MB | 0.41 | 59.36 | 693.0 | `tasks/alv-havener-e935fd-a7e56da5-v2` |
| [jackyzha0/quartz](https://github.com/jackyzha0/quartz) | typescript | 1 CPU / 1024 MB | 0.57 | 6.86 | 104.8 | `tasks/alv-quartz-a8b9bb-507ad7f3-v2` |
| [OAI/Arazzo-Specification](https://github.com/OAI/Arazzo-Specification) | javascript | 1 CPU / 1024 MB | 0.35 | 2.52 | 101.5 | `tasks/alv-arazzo-specification-f76518-a77e402c-v2` |
| [hashicorp/vault-action](https://github.com/hashicorp/vault-action) | javascript | 1 CPU / 1024 MB | 0.37 | 6.01 | 111.8 | `tasks/alv-vault-action-e4850f-2d6d66ae-v2` |
| [ota-meshi/eslint-plugin-yml](https://github.com/ota-meshi/eslint-plugin-yml) | typescript | 1 CPU / 1024 MB | 0.63 | 18.76 | 180.0 | `tasks/alv-eslint-plugin-yml-6c3aea-4dc06b25-v2` |
| [apache/cordova-cli](https://github.com/apache/cordova-cli) | javascript | 1 CPU / 1024 MB | 0.45 | 7.28 | 135.8 | `tasks/alv-cordova-cli-4371d8-f4ecbd1b-v2` |
| [mahendrapaipuri/grafana-dashboard-reporter-app](https://github.com/mahendrapaipuri/grafana-dashboard-reporter-app) | go | 1 CPU / 1024 MB | 0.56 | 37.69 | 517.0 | `tasks/alv-grafana-dashboard-re-6aea2c-8118343d-v2` |
| [mainmatter/gerust](https://github.com/mainmatter/gerust) | rust | 1 CPU / 1024 MB | 0.47 | 1.93 | 73.1 | `tasks/alv-gerust-fc6c9a-dc51688d-v2` |
| [Ingenimax/agent-sdk-go](https://github.com/Ingenimax/agent-sdk-go) | go | 1 CPU / 1024 MB | 0.63 | 118.02 | 604.9 | `tasks/alv-agent-sdk-go-5b059e-3739488a-v2` |
| [Keats/validator](https://github.com/Keats/validator) | rust | 1 CPU / 1024 MB | 0.41 | 76.24 | 352.2 | `tasks/alv-validator-b91cc2-68f2e33d-v2` |
| [rust-minidump/rust-minidump](https://github.com/rust-minidump/rust-minidump) | rust | 1 CPU / 1024 MB | 0.43 | 66.82 | 581.5 | `tasks/alv-rust-minidump-b32ba9-0155eaf7-v2` |
| [Kludex/starlette](https://github.com/Kludex/starlette) | python | 1 CPU / 1024 MB | 0.48 | 8.54 | 184.0 | `tasks/alv-starlette-59095f-5174d4c8-v2` |
| [antoniorodr/memo](https://github.com/antoniorodr/memo) | python | 1 CPU / 1024 MB | 0.46 | 2.19 | 52.2 | `tasks/alv-memo-0a5433-aafad4c9-v2` |
| [gadomski/antimeridian](https://github.com/gadomski/antimeridian) | python | 1 CPU / 1024 MB | 0.47 | 2.29 | 55.6 | `tasks/alv-antimeridian-f392be-5280e7fc-v2` |
| [dajiaji/pyseto](https://github.com/dajiaji/pyseto) | python | 1 CPU / 1024 MB | 0.5 | 21.1 | 327.8 | `tasks/alv-pyseto-18e9fe-f2f9e92c-v2` |
| [unfoldadmin/django-unfold](https://github.com/unfoldadmin/django-unfold) | python | 1 CPU / 1024 MB | 0.45 | 45.41 | 155.8 | `tasks/alv-django-unfold-7c5f7e-456ede4b-v2` |
| [hashicorp/terraform-plugin-go](https://github.com/hashicorp/terraform-plugin-go) | go | 1 CPU / 1024 MB | 0.56 | 25.44 | 237.0 | `tasks/alv-terraform-plugin-go-518f80-734544cd-v2` |
| [hashicorp/terraform-plugin-framework](https://github.com/hashicorp/terraform-plugin-framework) | go | 1 CPU / 1024 MB | 0.57 | 71.5 | 469.3 | `tasks/alv-terraform-plugin-fra-e4480f-a0219204-v2` |
| [solo-agent/solo](https://github.com/solo-agent/solo) | go | 1 CPU / 1024 MB | 0.52 | 28.93 | 305.9 | `tasks/alv-solo-9bfcd9-835c30f5-v2` |
| [hashicorp/terraform-json](https://github.com/hashicorp/terraform-json) | go | 1 CPU / 1024 MB | 0.57 | 16.21 | 129.6 | `tasks/alv-terraform-json-ec6f75-f4ef9969-v2` |
| [RSeidelsohn/license-checker-rseidelsohn](https://github.com/RSeidelsohn/license-checker-rseidelsohn) | typescript | 1 CPU / 1024 MB | 0.44 | 25.75 | 284.7 | `tasks/alv-license-checker-rsei-83c0ed-3d285180-v2` |
| [hashicorp/terraform-plugin-docs](https://github.com/hashicorp/terraform-plugin-docs) | go | 1 CPU / 1024 MB | 0.46 | 19.95 | 216.4 | `tasks/alv-terraform-plugin-doc-ff928b-b766be14-v2` |
| [bpmn-io/moddle](https://github.com/bpmn-io/moddle) | javascript | 1 CPU / 1024 MB | 0.39 | 2.52 | 70.4 | `tasks/alv-moddle-e7ab56-3124e6ac-v2` |
| [hashicorp/terraform-provider-archive](https://github.com/hashicorp/terraform-provider-archive) | go | 1 CPU / 1024 MB | 0.37 | 40.53 | 369.2 | `tasks/alv-terraform-provider-a-0d7c1e-44050a6f-v2` |
| [Fannon/search-bookmarks-history-and-tabs](https://github.com/Fannon/search-bookmarks-history-and-tabs) | javascript | 1 CPU / 1024 MB | 0.58 | 30.87 | 465.7 | `tasks/alv-search-bookmarks-his-1f8492-39397a86-v2` |
| [Vladimir-Urik/OxMgr](https://github.com/Vladimir-Urik/OxMgr) | rust | 1 CPU / 1024 MB | 0.46 | 6.29 | 57.5 | `tasks/alv-oxmgr-7856c0-2f4f0224-v2` |
| [FairwindsOps/polaris](https://github.com/FairwindsOps/polaris) | go | 1 CPU / 1024 MB | 0.55 | 74.61 | 756.2 | `tasks/alv-polaris-a9c480-4bdf5315-v2` |
| [rust-lang/libz-sys](https://github.com/rust-lang/libz-sys) | rust | 1 CPU / 1024 MB | 0.38 | 2.92 | 66.7 | `tasks/alv-libz-sys-39fce7-7ceb9154-v2` |
| [rust-vmm/seccompiler](https://github.com/rust-vmm/seccompiler) | rust | 1 CPU / 1024 MB | 0.5 | 4.53 | 121.5 | `tasks/alv-seccompiler-84db25-c05f2079-v2` |
| [kkawakam/rustyline](https://github.com/kkawakam/rustyline) | rust | 1 CPU / 1024 MB | 0.45 | 10.25 | 242.9 | `tasks/alv-rustyline-787f45-6f20abaa-v2` |
| [the-lean-crate/cargo-diet](https://github.com/the-lean-crate/cargo-diet) | rust | 1 CPU / 1024 MB | 0.48 | 4.83 | 84.7 | `tasks/alv-cargo-diet-009208-9abdacab-v2` |
| [langgenius/dify-plugin-sdks](https://github.com/langgenius/dify-plugin-sdks) | python | 1 CPU / 1024 MB | 0.49 | 12.3 | 85.3 | `tasks/alv-dify-plugin-sdks-6f5df2-63556960-v2` |
| [ruvnet/midstream](https://github.com/ruvnet/midstream) | rust | 1 CPU / 1024 MB | 0.49 | 9.46 | 116.8 | `tasks/alv-midstream-89f6ee-92250c20-v2` |
| [CycloneDX/cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib) | python | 1 CPU / 1024 MB | 0.47 | 24.19 | 113.8 | `tasks/alv-cyclonedx-python-lib-d5d8b1-cfc8221b-v2` |
| [bluekeyes/go-gitdiff](https://github.com/bluekeyes/go-gitdiff) | go | 1 CPU / 1024 MB | 0.45 | 7.68 | 96.4 | `tasks/alv-go-gitdiff-0bebda-b25b7331-v2` |
| [ugzv/ublockdnsclient](https://github.com/ugzv/ublockdnsclient) | go | 1 CPU / 1024 MB | 0.52 | 13.13 | 150.3 | `tasks/alv-ublockdnsclient-2e2c21-3297261f-v2` |
| [reg-viz/img-diff-js](https://github.com/reg-viz/img-diff-js) | typescript | 1 CPU / 1024 MB | 0.57 | 7.56 | 251.6 | `tasks/alv-img-diff-js-36b956-6860573a-v2` |
| [quic-go/webtransport-go](https://github.com/quic-go/webtransport-go) | go | 1 CPU / 1024 MB | 0.51 | 20.83 | 170.5 | `tasks/alv-webtransport-go-23cbff-23b4cd14-v2` |
| [goss-org/goss](https://github.com/goss-org/goss) | go | 1 CPU / 1024 MB | 0.55 | 25.02 | 235.8 | `tasks/alv-goss-bebd7b-582ab7d7-v2` |
| [mnemon-dev/mnemon](https://github.com/mnemon-dev/mnemon) | go | 1 CPU / 1024 MB | 0.55 | 49.0 | 732.4 | `tasks/alv-mnemon-d2c0f4-39a175e9-v2` |
| [interuss/dss](https://github.com/interuss/dss) | go | 1 CPU / 1024 MB | 0.61 | 42.41 | 443.7 | `tasks/alv-dss-2d6e9d-f8402882-v2` |
| [git-pkgs/git-pkgs](https://github.com/git-pkgs/git-pkgs) | go | 1 CPU / 1024 MB | 0.44 | 49.11 | 790.2 | `tasks/alv-git-pkgs-740bb5-5d07a00b-v2` |
| [slackapi/slack-github-action](https://github.com/slackapi/slack-github-action) | javascript | 1 CPU / 1024 MB | 0.4 | 5.9 | 115.9 | `tasks/alv-slack-github-action-5f0f34-e23ce5f2-v2` |
| [ilai-deutel/kibi](https://github.com/ilai-deutel/kibi) | rust | 1 CPU / 1024 MB | 0.42 | 4.15 | 82.2 | `tasks/alv-kibi-fb032c-4b756e0b-v2` |
| [NUKnightLab/TimelineJS3](https://github.com/NUKnightLab/TimelineJS3) | javascript | 1 CPU / 1024 MB | 0.45 | 8.39 | 180.9 | `tasks/alv-timelinejs3-dcc18e-27f700ed-v2` |
| [jscad/OpenJSCAD.org](https://github.com/jscad/OpenJSCAD.org) | javascript | 1 CPU / 1024 MB | 0.49 | 116.12 | 205.6 | `tasks/alv-openjscad-org-36e7d2-f245ea3a-v2` |
| [jeremydaly/lambda-api](https://github.com/jeremydaly/lambda-api) | javascript | 1 CPU / 1024 MB | 0.63 | 29.23 | 339.7 | `tasks/alv-lambda-api-ab6995-c7d876f7-v2` |
| [thatmagicalcat/txm](https://github.com/thatmagicalcat/txm) | rust | 1 CPU / 1024 MB | 0.48 | 3.57 | 89.6 | `tasks/alv-txm-cf5a89-26e6d3cf-v2` |
| [mimblewimble/grin](https://github.com/mimblewimble/grin) | rust | 1 CPU / 1024 MB | 0.4 | 2.05 | 85.4 | `tasks/alv-grin-ba61b0-e4c4a388-v2` |
| [LiveSplit/livesplit-core](https://github.com/LiveSplit/livesplit-core) | rust | 1 CPU / 1024 MB | 0.52 | 14.53 | 332.8 | `tasks/alv-livesplit-core-49b9a9-f26195cd-v2` |
| [michel-kraemer/zsh-patina](https://github.com/michel-kraemer/zsh-patina) | rust | 1 CPU / 1024 MB | 0.51 | 63.7 | 79.1 | `tasks/alv-zsh-patina-cc5077-3d980f07-v2` |
| [zeqianli/tgv](https://github.com/zeqianli/tgv) | rust | 1 CPU / 1024 MB | 0.45 | 12.73 | 183.0 | `tasks/alv-tgv-89df2b-0f634f9d-v2` |
| [Kohei-Wada/taskdog](https://github.com/Kohei-Wada/taskdog) | python | 1 CPU / 1024 MB | 0.48 | 8.6 | 94.7 | `tasks/alv-taskdog-831fec-f121db94-v2` |
| [9001/copyparty](https://github.com/9001/copyparty) | python | 1 CPU / 1024 MB | 0.41 | 14.32 | 80.9 | `tasks/alv-copyparty-8f9592-398fcf1d-v2` |
| [pytest-dev/pytest-xdist](https://github.com/pytest-dev/pytest-xdist) | python | 1 CPU / 1024 MB | 0.43 | 55.57 | 52.1 | `tasks/alv-pytest-xdist-d07681-bda3903d-v2` |
| [mccutchen/go-httpbin](https://github.com/mccutchen/go-httpbin) | go | 1 CPU / 1024 MB | 0.55 | 21.9 | 147.5 | `tasks/alv-go-httpbin-6d9717-697b6e3b-v2` |
| [prometheus-community/elasticsearch_exporter](https://github.com/prometheus-community/elasticsearch_exporter) | go | 1 CPU / 1024 MB | 0.67 | 21.06 | 244.2 | `tasks/alv-elasticsearch-export-0f7801-43f5e916-v2` |
| [sevensolutions/traefik-oidc-auth](https://github.com/sevensolutions/traefik-oidc-auth) | go | 1 CPU / 1024 MB | 0.54 | 11.14 | 135.0 | `tasks/alv-traefik-oidc-auth-07c6eb-96ca84ff-v2` |
| [prometheus-community/postgres_exporter](https://github.com/prometheus-community/postgres_exporter) | go | 1 CPU / 1024 MB | 0.41 | 20.23 | 190.9 | `tasks/alv-postgres-exporter-384d86-eaa67f02-v2` |
| [dm-p/powerbi-visuals-html-content](https://github.com/dm-p/powerbi-visuals-html-content) | typescript | 1 CPU / 1024 MB | 0.48 | 21.22 | 160.0 | `tasks/alv-powerbi-visuals-html-df152d-0161a416-v2` |
| [heroku/terraform-provider-heroku](https://github.com/heroku/terraform-provider-heroku) | go | 1 CPU / 1024 MB | 0.53 | 25.0 | 326.1 | `tasks/alv-terraform-provider-h-72f983-1ffae974-v2` |
| [yonahd/kor](https://github.com/yonahd/kor) | go | 1 CPU / 1024 MB | 0.49 | 80.43 | 708.2 | `tasks/alv-kor-2e923a-7a30ce11-v2` |
| [elm-tooling/elm-language-server](https://github.com/elm-tooling/elm-language-server) | typescript | 1 CPU / 1024 MB | 0.62 | 86.59 | 589.1 | `tasks/alv-elm-language-server-9d490f-33bc547c-v2` |
| [in-toto/witness](https://github.com/in-toto/witness) | go | 1 CPU / 1024 MB | 0.47 | 73.16 | 695.3 | `tasks/alv-witness-20a597-9f326827-v2` |
| [test-results-reporter/testbeats](https://github.com/test-results-reporter/testbeats) | javascript | 1 CPU / 1024 MB | 0.48 | 6.48 | 94.2 | `tasks/alv-testbeats-6d30e7-003f1fae-v2` |
| [serde-rs/serde](https://github.com/serde-rs/serde) | rust | 1 CPU / 1024 MB | 0.45 | 12.87 | 172.8 | `tasks/alv-serde-53097d-747814f7-v2` |
| [coder3101/protols](https://github.com/coder3101/protols) | rust | 1 CPU / 1024 MB | 0.41 | 2.67 | 57.9 | `tasks/alv-protols-697906-b2e91401-v2` |
| [untitaker/html5gum](https://github.com/untitaker/html5gum) | rust | 1 CPU / 1024 MB | 0.51 | 45.61 | 176.2 | `tasks/alv-html5gum-32d416-b43d5ed3-v2` |
| [jonasbb/serde_with](https://github.com/jonasbb/serde_with) | rust | 1 CPU / 1024 MB | 0.52 | 46.36 | 333.4 | `tasks/alv-serde-with-a47a40-8c8805c6-v2` |
| [polarity-lang/polarity](https://github.com/polarity-lang/polarity) | rust | 1 CPU / 1024 MB | 0.54 | 3.49 | 110.2 | `tasks/alv-polarity-2d31e2-325629ea-v2` |
| [bitwarden/agent-access](https://github.com/bitwarden/agent-access) | rust | 1 CPU / 1024 MB | 0.49 | 23.83 | 230.7 | `tasks/alv-agent-access-eeb57b-9cd303f6-v2` |
| [rcieri/glab-tui](https://github.com/rcieri/glab-tui) | rust | 2 CPU / 4096 MB | 0.41 | 5.86 | 61.2 | `tasks/alv-glab-tui-8439bc-72b962f4-v2` |
| [aws-actions/aws-cloudformation-github-deploy](https://github.com/aws-actions/aws-cloudformation-github-deploy) | typescript | 2 CPU / 4096 MB | 0.56 | 30.47 | 785.1 | `tasks/alv-aws-cloudformation-g-a1c8ab-197fa4ac-v2` |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | rust | 2 CPU / 4096 MB | 0.47 | 15.89 | 79.1 | `tasks/alv-rtk-dc41af-8a24ce2e-v2` |
| [tailscale/tailscale-rs](https://github.com/tailscale/tailscale-rs) | rust | 2 CPU / 4096 MB | 0.69 | 60.89 | 1299.3 | `tasks/alv-tailscale-rs-dc89ee-19d3bad0-v2` |
| [josh-project/josh](https://github.com/josh-project/josh) | rust | 2 CPU / 4096 MB | 0.55 | 39.04 | 1524.7 | `tasks/alv-josh-5eb525-760ab472-v2` |
| [slackapi/bolt-js](https://github.com/slackapi/bolt-js) | typescript | 2 CPU / 4096 MB | 0.61 | 65.39 | 724.6 | `tasks/alv-bolt-js-6e7cfb-4f8d888b-v2` |
| [xataio/pgstream](https://github.com/xataio/pgstream) | go | 2 CPU / 4096 MB | 0.51 | 97.71 | 1624.4 | `tasks/alv-pgstream-b63187-40c34364-v2` |
| [mierak/rmpc](https://github.com/mierak/rmpc) | rust | 2 CPU / 4096 MB | 0.48 | 4.79 | 95.2 | `tasks/alv-rmpc-c6565d-500a1de7-v2` |
| [marmotdata/marmot](https://github.com/marmotdata/marmot) | go | 2 CPU / 4096 MB | 0.42 | 63.97 | 1290.7 | `tasks/alv-marmot-837b39-b3ebf2a0-v2` |
| [typstyle-rs/typstyle](https://github.com/typstyle-rs/typstyle) | rust | 2 CPU / 4096 MB | 0.55 | 90.88 | 347.5 | `tasks/alv-typstyle-83473d-8a3c6e20-v2` |
| [LukasNiessen/ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) | typescript | 2 CPU / 4096 MB | 0.43 | 11.68 | 502.0 | `tasks/alv-archunitts-c5f5b0-4a2a8a71-v2` |
| [iced-rs/iced](https://github.com/iced-rs/iced) | rust | 2 CPU / 4096 MB | 0.53 | 18.82 | 325.8 | `tasks/alv-iced-617f16-3c81aac2-v2` |
| [temporalio/temporal-worker-controller](https://github.com/temporalio/temporal-worker-controller) | go | 2 CPU / 4096 MB | 0.48 | 103.63 | 2118.2 | `tasks/alv-temporal-worker-cont-543b71-01a92a04-v2` |
| [kubestellar/kubeflex](https://github.com/kubestellar/kubeflex) | go | 2 CPU / 4096 MB | 0.48 | 7.68 | 215.5 | `tasks/alv-kubeflex-135d51-d6e22825-v2` |
| [s3s-project/s3s](https://github.com/s3s-project/s3s) | rust | 2 CPU / 4096 MB | 0.53 | 31.11 | 590.1 | `tasks/alv-s3s-aa8567-1c248a36-v2` |
| [e-breuninger/terraform-provider-netbox](https://github.com/e-breuninger/terraform-provider-netbox) | go | 2 CPU / 4096 MB | 0.57 | 40.85 | 732.2 | `tasks/alv-terraform-provider-n-101b3c-f24313e0-v2` |
| [apollographql/apollo-mcp-server](https://github.com/apollographql/apollo-mcp-server) | rust | 2 CPU / 4096 MB | 0.49 | 26.66 | 273.0 | `tasks/alv-apollo-mcp-server-0c4dce-c628a77d-v2` |
| [kittors/CliRelay](https://github.com/kittors/CliRelay) | go | 2 CPU / 4096 MB | 0.64 | 94.83 | 718.7 | `tasks/alv-clirelay-9b6159-e6ccaf51-v2` |
| [stackql/stackql](https://github.com/stackql/stackql) | go | 2 CPU / 4096 MB | 0.56 | 93.4 | 820.4 | `tasks/alv-stackql-9aba5a-d9185df8-v2` |
| [cloudnativelabs/kube-router](https://github.com/cloudnativelabs/kube-router) | go | 2 CPU / 4096 MB | 0.42 | 82.49 | 1148.7 | `tasks/alv-kube-router-b9cf3d-dde22778-v2` |
| [txpipe/dolos](https://github.com/txpipe/dolos) | rust | 2 CPU / 4096 MB | 0.56 | 30.25 | 515.7 | `tasks/alv-dolos-bc7509-b7daa48c-v2` |
| [pamburus/hl](https://github.com/pamburus/hl) | rust | 2 CPU / 4096 MB | 0.61 | 20.09 | 461.4 | `tasks/alv-hl-ddc322-e0f44223-v2` |
| [boyter/scc](https://github.com/boyter/scc) | go | 2 CPU / 4096 MB | 0.61 | 19.95 | 832.8 | `tasks/alv-scc-93a6ef-90d36ed2-v2` |
| [arlyon/async-stripe](https://github.com/arlyon/async-stripe) | rust | 2 CPU / 4096 MB | 0.51 | 48.16 | 914.4 | `tasks/alv-async-stripe-b9d314-3ccf2994-v2` |
| [tqwewe/kameo](https://github.com/tqwewe/kameo) | rust | 2 CPU / 4096 MB | 0.51 | 66.51 | 1210.8 | `tasks/alv-kameo-e8a8d4-b4aaee79-v2` |
| [0sec-labs/foxguard](https://github.com/0sec-labs/foxguard) | rust | 2 CPU / 4096 MB | 0.45 | 25.34 | 297.6 | `tasks/alv-foxguard-8a1267-40eeccdc-v2` |
| [keepsimple1/mdns-sd](https://github.com/keepsimple1/mdns-sd) | rust | 2 CPU / 4096 MB | 0.52 | 73.1 | 146.2 | `tasks/alv-mdns-sd-d203c1-30432c20-v2` |
| [burningalchemist/sql_exporter](https://github.com/burningalchemist/sql_exporter) | go | 2 CPU / 4096 MB | 0.6 | 40.34 | 1160.9 | `tasks/alv-sql-exporter-71a54d-648fd0c4-v2` |
| [rayfish/rayfish](https://github.com/rayfish/rayfish) | rust | 2 CPU / 4096 MB | 0.59 | 62.87 | 2574.4 | `tasks/alv-rayfish-47489a-e07d7959-v2` |
| [virtual-kubelet/virtual-kubelet](https://github.com/virtual-kubelet/virtual-kubelet) | go | 2 CPU / 4096 MB | 0.52 | 119.39 | 1085.3 | `tasks/alv-virtual-kubelet-68a94c-4c39a8e1-v2` |

## Logs

Raw stage logs are under `/home/xubingyu/AlvanceGithubCrawler/outputs/production-runs/github-mass-production-XBY-20260730/logs`.
