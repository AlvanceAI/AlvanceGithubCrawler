为 FFmpeg 命令生成器增加原生 VAAPI 硬件加速支持，根据配置生成 h264_vaapi、vaapi 像素格式与 scale_vaapi 滤镜，并避免对快照命令注入不兼容的视频滤镜。
