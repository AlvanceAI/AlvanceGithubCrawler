移除公开的 `pixels::SurfaceTexture` 封装，改由 `PixelsBuilder` 接收窗口句柄和公开可配置的 `wgpu::SurfaceConfiguration`，并让 `Pixels` 持有该配置以供表面重配置复用。
