//
//  Shaders.metal
//  chapter03
//
//  Created by Marius on 1/12/16.
//  Copyright © 2016 Marius Horga. All rights reserved.
//

// [https://github.com/MetalKit/metal/blob/master/ch03/chapter03/Shaders.metal](https://github.com/MetalKit/metal/blob/master/ch03/chapter03/Shaders.metal)

#include <metal_stdlib>
using namespace metal;

struct Vertex {
    float4 position [[position]];
};

vertex Vertex vertex_func(constant Vertex *vertices [[buffer(0)]],
                          uint vid [[vertex_id]]) {
    return vertices[vid];
}

fragment float4 fragment_func(Vertex vert [[stage_in]]) {
    return float4(0.7, 1, 1, 1);
}
