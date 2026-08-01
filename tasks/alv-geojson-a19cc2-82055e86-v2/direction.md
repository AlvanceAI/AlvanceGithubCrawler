统一 GeoJSON 反序列化行为，使 loads() 对可解析的 JSON 对象始终返回具有 is_valid 等接口的 GeoJSON 对象，而不是在无法识别类型时退回原生 dict。
