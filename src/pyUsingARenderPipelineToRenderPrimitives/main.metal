#include <metal_stdlib>
#include <simd/simd.h>

using namespace metal;

typedef enum AAPLVertexInputIndex
{
  AAPLVertexInputIndexVertices     = 0,
  AAPLVertexInputIndexViewportSize = 1,
} AAPLVertexInputIndex;

typedef struct
{
  vector_float2 position;
  vector_float4 color;
} AAPLVertex;

struct RasterizerData
{
  float4 position [[position]];
  float4 color;
};



vertex RasterizerData
vertexShader(uint vertexID [[vertex_id]],
             constant AAPLVertex *vertices [[buffer(AAPLVertexInputIndexVertices)]],
             constant vector_uint2 *viewportSizePointer [[buffer(AAPLVertexInputIndexViewportSize)]])
{
  RasterizerData out;
  
  float2 pixelSpacePosition = vertices[vertexID].position.xy;
  
  vector_float2 viewportSize = vector_float2(*viewportSizePointer);
  
  out.position = vector_float4(0.0, 0.0, 0.0, 1.0);
  out.position.xy = pixelSpacePosition / (viewportSize / 2.0);
  out.color = vertices[vertexID].color;

  return out;
}

fragment float4 fragmentShader(RasterizerData in [[stage_in]])
{
  return in.color;
}


