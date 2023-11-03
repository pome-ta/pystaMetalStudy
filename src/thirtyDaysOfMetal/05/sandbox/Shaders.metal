// [https://github.com/metal-by-example/thirty-days-of-metal/blob/master/05/MetalShaders/MetalShaders/Sh](https://github.com/metal-by-example/thirty-days-of-metal/blob/master/05/MetalShaders/MetalShaders/Shaders.metal)



#include <metal_stdlib>
using namespace metal;

vertex float4 vertex_main(device float2 const* positions [[buffer(0)]],
                          uint vertexID [[vertex_id]])
{
    float2 position = positions[vertexID];
    return float4(position, 0.0, 1.0);
}

fragment float4 fragment_main(float4 position [[stage_in]]) {
    return float4(1.0, 0.0, 0.0, 1.0);
}
