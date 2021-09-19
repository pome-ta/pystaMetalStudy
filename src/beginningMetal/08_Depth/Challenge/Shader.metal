//
//  Shader.metal
//  MacOSGimma
//
//  Created by Jaap Wijnen on 05/02/2017.
//  Copyright © 2017 Workmoose. All rights reserved.
//

// https://github.com/JaapWijnen/MacOSGimma/blob/master/MacOSGimma/Shader.metal

#include <metal_stdlib>
using namespace metal;

struct ModelConstants {
    float4x4 modelViewMatrix;
};

struct SceneConstants {
    float4x4 projectionMatrix;
};

struct VertexIn {
    float4 position [[ attribute(0) ]];
    float4 color [[ attribute(1) ]];
    float2 textureCoordinates [[ attribute(2) ]];
};

struct VertexOut {
    float4 position [[ position ]];
    float4 color;
    float2 textureCoordinates;
};

vertex VertexOut vertex_shader(const VertexIn vertexIn [[ stage_in ]],
                               constant ModelConstants &modelConstants [[ buffer(1) ]],
                               constant SceneConstants &sceneConstants [[ buffer(2) ]])  {
    
    VertexOut vertexOut;
    
    float4x4 matrix = sceneConstants.projectionMatrix * modelConstants.modelViewMatrix;
    vertexOut.position = matrix * vertexIn.position;
    
    vertexOut.color = vertexIn.color;
    vertexOut.textureCoordinates = vertexIn.textureCoordinates;
    
    return vertexOut;
}

fragment half4 fragment_shader(VertexOut vertexIn [[ stage_in ]]) {
    return half4(vertexIn.color);
}

fragment half4 textured_fragment(VertexOut vertexIn [[ stage_in ]],
                                 sampler sampler2d [[ sampler(0) ]],
                                 texture2d<float> texture [[ texture(0) ]] ) {
    float4 color = texture.sample(sampler2d, vertexIn.textureCoordinates);
    if (color.a == 0.0)
        discard_fragment();
    return half4(color.r, color.g, color.b, 1);
}

fragment half4 textured_mask_fragment(VertexOut vertexIn [[ stage_in ]],
                                      texture2d<float> texture [[ texture(0) ]],
                                      texture2d<float> maskTexture [[ texture(1) ]],
                                      sampler sampler2d [[ sampler(0) ]] ) {
    float4 color = texture.sample(sampler2d, vertexIn.textureCoordinates);
    float4 maskColor = maskTexture.sample(sampler2d, vertexIn.textureCoordinates);
    float maskOpacity = maskColor.a;
    if (maskOpacity < 0.5)
        discard_fragment();
    return half4(color.r, color.g, color.b, 1);
}
