//
//  Shaders.metal
//  ExploringMetal
//
//  Created by Adil Patel on 31/05/2018.
//  Copyright © 2018 Adil Patel. All rights reserved.
//

// File for Metal kernel and shader functions

#include <metal_stdlib>
#include <simd/simd.h>

using namespace metal;

// The structure that is fed into the vertex shader. We use packed data types to alleviate memory alignment
// issues caused by the float2
typedef struct {
    packed_float2 position;
    packed_float4 colour;
} Vertex;

// The output of the vertex shader, which will be fed into the fragment shader
typedef struct {
    float4 position [[position]];
    float4 colour;
} RasteriserData;

vertex RasteriserData helloVertexShader(uint vertexID [[vertex_id]],
                                        constant Vertex *vertices [[buffer(0)]]) {
    
    RasteriserData out;
    out.position = float4(0.0, 0.0, 0.0, 1.0);
    out.position.xy = vertices[vertexID].position;
    out.colour = vertices[vertexID].colour;

    // Both the colour and the clip space position will be interpolated in this data structure
    return out;
}

fragment float4 helloFragmentShader(RasteriserData in [[stage_in]]) {
    return in.colour;
}
