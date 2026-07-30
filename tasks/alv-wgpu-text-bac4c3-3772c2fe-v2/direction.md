为 BrushBuilder 增加共享渲染管线的构建能力，使多个 TextBrush 能复用同一个 wgpu::RenderPipeline，同时各自保留独立的字形缓存、纹理资源和顶点缓冲区。
