Repository `beaufour/flickr-download` at commit `e5516da3feb31c03024571ad8ea674804f121922` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

在下载 photoset 时通过 PhotoSet.getPhotos 的 extras 直接复用照片元数据，并引入支持预加载元数据的 Photo 实现，避免对每张照片重复调用 getInfo() 和 getSizes()。
