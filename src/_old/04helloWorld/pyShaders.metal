// [[macOS][Metal]MetalKit入門](https://qiita.com/m_yukio/items/d3eaad6326c4b4b0f5d1)

#include <metal_stdlib>
using namespace metal;

struct Vertex {
    float4 position [[position]];
    float4 color;
};
 
vertex Vertex vertex_func(constant Vertex *vertices [[buffer(0)]],
                          uint vid [[vertex_id]]) {
    return vertices[vid];
}
 
fragment float4 fragment_func(Vertex vert [[stage_in]]) {
    float3 inColor = float3(vert.color.x, vert.color.y, vert.color.z);
    float4 outColor = float4(inColor.x, inColor.y, inColor.z, 1);
    return outColor;
}

