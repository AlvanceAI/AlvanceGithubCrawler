Repository `parasyte/pixels` at commit `47c09b923d9a646fe6d71515edcc497156f4f356` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

移除公开的 `pixels::SurfaceTexture` 封装，改由 `PixelsBuilder` 接收窗口句柄和公开可配置的 `wgpu::SurfaceConfiguration`，并让 `Pixels` 持有该配置以供表面重配置复用。
