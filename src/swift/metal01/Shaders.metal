//
//  Shaders.metal
//  metal01
//
//  Created by pome-ta on 2021/07/16.
//

#include <metal_stdlib>
using namespace metal;

#include "ShaderDefinitions.h"

struct VertexOut {
    float4 color;
    float4 pos [[position]];
};


vertex VertexOut vertexShader(const device Vertex *vertexArray [[buffer(0)]], unsigned int vid [[vertex_id]])
{
    // TODO: Write vertex shader
    Vertex in = vertexArray[vid];
    VertexOut out;

    // Pass the vertex color directly to the rasterizer
    out.color = in.color;
    out.pos = float4(in.pos.x, in.pos.y, 0, 1);

    return out;

}

fragment float4 fragmentShader(VertexOut interpolated [[stage_in]])
{
    // TODO: Write fragment shader
    return interpolated.color;

}
