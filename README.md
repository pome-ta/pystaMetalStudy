# pystaMetalStudy

[Pythonista 3](http://omz-software.com/pythonista/) でMetal をチャレンジするリポリトリ

さまざまなサイトを参照しているので、参照URL などは、各ディレクトリ内に明記予定


以下列記は、実装日誌的なメモ


# 📝 2026/02/23

[pystaRubiconObjcSandBox/playground/Metal/BeginningMetal at main · pome-ta/pystaRubiconObjcSandBox](https://github.com/pome-ta/pystaRubiconObjcSandBox/tree/main/playground/Metal/BeginningMetal)

rubicon でMetal を再度挑戦中。


# 📝 2023/10/19


過去の困りを確認しようとしても、困ってるお気持ちしか書いてないので、キャッチアップできない


困りのコードと、期待値と結果程度は残すようにしたい



## [src/everythingAboutTheMetalAPI/chapter04/sandbox/231019_0004.py](https://github.com/pome-ta/pystaMetalStudy/blob/main/src/everythingAboutTheMetalAPI/chapter04/sandbox/231019_0004.py)


numpy で構造体を書いてみてる

サイズの取り方とか、どうかなぁ、、、


[NumPy - Structured arrays](https://runebook.dev/ja/docs/numpy/user/basics.rec#numpy.lib.recfunctions.repack_fields)



## ヘッダーファイルの取り込み

目算がついていない


`.metal` に直書きにするとしても、cpu 側でのパスすることを確認しなければ、、、


[[Metal]metalファイルをプリコンパイルしつつ実機でもコンパイルする #iOS - Qiita](https://qiita.com/noppefoxwolf/items/ddfec339f6002a33bc3b)

[[Metal]MTLLibraryをランタイムでコンパイルする #iOS - Qiita](https://qiita.com/noppefoxwolf/items/fe6ea83f0e0e9703033c)


[User defined. What I typically do is 1) add some sensible defaults to the top of my shader code so that I can use a precompiled library if I choose: #ifndef THREADS_PER_THREADGROUP #define... - Matthew Kieber-Emmons - Medium](https://kieber-emmons.medium.com/user-defined-3767eb5bfee4)


# 📝 2023/10/10

## `ui` モジュール依存を剥がす

ちまちまと、やってく

## 📝 2022/10/07

simd 調査？


## 📝 2022/04/22

```
n0	simd::float3	(-0, -0.707106649, -0, -0)	
[0]	float	-0
[1]	float	-0.707106649
[2]	float	-0
[3]	float	-0
v0	simd::float3	(-0.25, 1.99000001, -0.25, 1)	
[0]	float	-0.25
[1]	float	1.99000001
[2]	float	-0.25
[3]	float	1
v1	simd::float3	(-0.25, 1.99000001, 0.25, 1)	
[0]	float	-0.25
[1]	float	1.99000001
[2]	float	0.25
[3]	float	1
v2	simd::float3	(0.25, 1.99000001, 0.25, 1)	
[0]	float	0.25
[1]	float	1.99000001
[2]	float	0.25
[3]	float	1
n1	simd::float3	(-0, -0.707106649, -0, -0)	
[0]	float	-0
[1]	float	-0.707106649
[2]	float	-0
[3]	float	-0
v3	simd::float3	(0.25, 1.99000001, -0.25, 1)	
[0]	float	0.25
[1]	float	1.99000001
[2]	float	-0.25
[3]	float	1
```

```
vertices	std::vector<float __attribute__((ext_vector_type(3))), std::allocator<float __attribute__((ext_vector_type(3)))> > &	size=6	0x00000001083dce80
[0]	float __attribute__((ext_vector_type(3)))	(-0.25, 1.99000001, -0.25, 1)	
[1]	float __attribute__((ext_vector_type(3)))	(-0.25, 1.99000001, 0.25, 1)	
[2]	float __attribute__((ext_vector_type(3)))	(0.25, 1.99000001, 0.25, 1)	
[3]	float __attribute__((ext_vector_type(3)))	(-0.25, 1.99000001, -0.25, 1)	
[4]	float __attribute__((ext_vector_type(3)))	(0.25, 1.99000001, 0.25, 1)	
[5]	float __attribute__((ext_vector_type(3)))	(0.25, 1.99000001, -0.25, 1)	
```




```
normals	std::vector<float __attribute__((ext_vector_type(3))), std::allocator<float __attribute__((ext_vector_type(3)))> > &	size=6	0x00000001045c6e98


[0]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	
[1]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	
[2]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	
[3]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	
[4]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	
[5]	float __attribute__((ext_vector_type(3)))	(-0, -0.707106649, -0, -0)	

```

```
colors	std::vector<float __attribute__((ext_vector_type(3))), std::allocator<float __attribute__((ext_vector_type(3)))> > &	size=6	0x00000001045c6eb0
[0]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
[1]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
[2]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
[3]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
[4]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
[5]	float __attribute__((ext_vector_type(3)))	(1, 1, 1, 0)	
```

```
color	simd::float3	(1, 1, 1, 0)	
```


## 📝 2021/12/11

### delegate

`__main__.py` での`addSubview_` は、class 定義したview を呼び出す



```.py
self.objc_instance.addSubview_({classのview})
```


### simd の演算

objc

```
cubeVertices	simd::float3 [8]	
  [0]	simd::float3	(-0.25, 0.00999999046, -0.25, 1)	
  [1]	simd::float3	(0.25, 0.00999999046, -0.25, 1)	
  [2]	simd::float3	(-0.25, 1.99000001, -0.25, 1)	
  [3]	simd::float3	(0.25, 1.99000001, -0.25, 1)	
  [4]	simd::float3	(-0.25, 0.00999999046, 0.25, 1)	
  [5]	simd::float3	(0.25, 0.00999999046, 0.25, 1)	
  [6]	simd::float3	(-0.25, 1.99000001, 0.25, 1)	
  [7]	simd::float3	(0.5, 0.5, 0.5, 0)	

```


```
transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [-0.5000, -0.5000, -0.5000, 1.0000]
matrixMULvertex: Vector4:
  [-0.2500, -0.9900, -0.2500, 0.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [0.5000, -0.5000, -0.5000, 1.0000]
matrixMULvertex: Vector4:
  [0.2500, -0.9900, -0.2500, 0.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [-0.5000, 0.5000, -0.5000, 1.0000]
matrixMULvertex: Vector4:
  [-0.2500, 0.9900, -0.2500, 1.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [0.5000, 0.5000, -0.5000, 1.0000]
matrixMULvertex: Vector4:
  [0.2500, 0.9900, -0.2500, 1.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [-0.5000, -0.5000, 0.5000, 1.0000]
matrixMULvertex: Vector4:
  [-0.2500, -0.9900, 0.2500, 0.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [0.5000, -0.5000, 0.5000, 1.0000]
matrixMULvertex: Vector4:
  [0.2500, -0.9900, 0.2500, 0.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [-0.5000, 0.5000, 0.5000, 1.0000]
matrixMULvertex: Vector4:
  [-0.2500, 0.9900, 0.2500, 1.5000]

transform: Matrix4:
  [0.5000, 0.0000, 0.0000, 0.0000]
  [0.0000, 1.9800, 0.0000, 0.0000]
  [0.0000, 0.0000, 0.5000, 0.0000]
  [0.0000, 1.0000, 0.0000, 1.0000]
transformedVertex: Vector4:
  [0.5000, 0.5000, 0.5000, 1.0000]
matrixMULvertex: Vector4:
  [0.2500, 0.9900, 0.2500, 1.5000]

```




## 📝 2021/12/06

前回のmatrix の素材をうまく生かしながら

実装をしていく予定！


ローテート関係が、ちょっと手こずりそう？


### ray tracing チャレンジ

数値のlog 取り


#### `testTransform`

``` .mm
float4x4 testTransform = matrix4x4_translation(0.3275f, 0.3f, 0.3725f);
```

```
Printing description of testTransform:
(simd::float4x4) testTransform = {
  simd_float4x4 = {
    columns = {
      [0] = (1, 0, 0, 0)
      [1] = (0, 1, 0, 0)
      [2] = (0, 0, 1, 0)
      [3] = (0.327499986, 0.300000012, 0.372500002, 1)
    }
  }
}
```


#### `testScale`

``` .mm
float4x4 testScale = matrix4x4_scale(0.6f, 0.6f, 0.6f);
```


```
Printing description of testScale:
(simd::float4x4) testScale = {
  simd_float4x4 = {
    columns = {
      [0] = (0.600000024, 0, 0, 0)
      [1] = (0, 0.600000024, 0, 0)
      [2] = (0, 0, 0.600000024, 0)
      [3] = (0, 0, 0, 1)
    }
  }
}
```

#### `testRotation`

``` .mm
float4x4 testRotation = matrix4x4_rotation(-0.3f, vector3(0.0f, 1.0f, 0.0f));
```

```
Printing description of testRotation:
(simd::float4x4) testRotation = {
  simd_float4x4 = {
    columns = {
      [0] = (0.955336511, 0, 0.295520186, 0)
      [1] = (0, 1, 0, 0)
      [2] = (-0.295520186, 0, 0.955336511, 0)
      [3] = (0, 0, 0, 1)
    }
  }
}
```


#### `transform`

``` .mm
transform = matrix4x4_translation(0.3275f, 0.3f, 0.3725f) *
            matrix4x4_rotation(-0.3f, vector3(0.0f, 1.0f, 0.0f)) *
            matrix4x4_scale(0.6f, 0.6f, 0.6f);
```

```
Printing description of transform:
(simd::float4x4) transform = {
  simd_float4x4 = {
    columns = {
      [0] = (0.573201954, 0, 0.177312121, 0)
      [1] = (0, 0.600000024, 0, 0)
      [2] = (-0.177312121, 0, 0.573201954, 0)
      [3] = (0.327499986, 0.300000012, 0.372500002, 1)
    }
  }
}
```




``` .mm
    float4x4 transform = matrix4x4_translation(0.0f, 1.0f, 0.0f) *
                         matrix4x4_scale(0.5f, 1.98f, 0.5f);
```

```
Printing description of transform:
(simd::float4x4) transform = {
  simd_float4x4 = {
    columns = {
      [0] = (0.5, 0, 0, 0)
      [1] = (0, 1.98000002, 0, 0)
      [2] = (0, 0, 0.5, 0)
      [3] = (0, 1, 0, 1)
    }
  }
}
```

``` .mm
    transform = matrix4x4_translation(0.0f, 1.0f, 0.0f) * matrix4x4_scale(2.0f, 2.0f, 2.0f);
```

```
Printing description of transform:
(simd::float4x4) transform = {
  simd_float4x4 = {
    columns = {
      [0] = (2, 0, 0, 0)
      [1] = (0, 2, 0, 0)
      [2] = (0, 0, 2, 0)
      [3] = (0, 1, 0, 1)
    }
  }
}
```





## 📝 2021/12/01

### 構造体をShader に投げると、メモリ（？）がズレる問題


Shaderコードを直接イジる


- `float3`
- `float`
- `float3`
- `float`


の構造を、




``` .metal
struct Light {
  float3 color;
  float ambientIntensity;
  float diffuseIntensity;
  float3 direction;
};
```

- `float4`
  - `float3` + `float`
- `float4`
  - `float3` + `float`


と、まとめて`Shader.metal` 上で、分解する



``` .metal
float3 light_color = float3(light.color.x, light.color.y, light.color.z);
float light_ambientIntensity = float(light.color.w);
float3 ambientColor = light_color * light_ambientIntensity;
  
```



## 📝 2021/11/29

### `Light` の構造体が、`Shader.metal` で読めてない件


`color` は読めているが、`ambientIntensity` に参照できていない

``` .py
class Light(ctypes.Structure):
  _fields_ = [
    ('color', Float3),
    ('ambientIntensity', (ctypes.c_float))
  ]
```

``` .metal
fragment half4 fragment_color(VertexOut vertexIn [[ stage_in ]]) {
  return half4(vertexIn.materialColor);
}

fragment half4 lit_textured_fragment(VertexOut vertexIn [[ stage_in ]],
                                 sampler sampler2d [[ sampler(0) ]],
                                 constant Light &light [[ buffer(3) ]],
                                 texture2d<float> texture [[ texture(0) ]] ) {
  float4 color = texture.sample(sampler2d, vertexIn.textureCoordinates);
  color = color * vertexIn.materialColor;
  
  // Ambient
  float3 ambientColor = light.color * light.ambientIntensity;
  
  // `light.ambientIntensity` が通らない
  
  color = color * float4(ambientColor, 1);
  if (color.a == 0.0)
    discard_fragment();
  return half4(color.r, color.g, color.b, 1);
}
```

### `mScene.py` での読み取り

どうも、関数での読み取りの際に、サイズ(int) での指定がうまくいっていないっぽい

`stride` の部分がキモっぽい

#### Python で私が書いているコード

``` .py
    commandEncoder.setFragmentBytes_length_atIndex_(
      ctypes.byref(self.light),
      ctypes.sizeof(Light), 3)
```

#### 参照先のSwift のコード


``` .swift
// 関数が古いのは無視で
commandEncoder.setFragmentBytes(&light, length: MemoryLayout<Light>.stride, at: 3)
```

### log とり

疑似的なコードから、数値を抜き出す


``` .swift
light.color = float3(0,0,1)
light.ambientIntensity = 0.5
dump(light)
print("light ---")
print(MemoryLayout<Light>.stride)
print(MemoryLayout<Light>.size)
print(MemoryLayout<Light>.alignment)
print("float3 ---")
print(MemoryLayout<float3>.stride)
print(MemoryLayout<float3>.size)
print(MemoryLayout<float3>.alignment)
print("Float ---")
print(MemoryLayout<Float>.stride)
print(MemoryLayout<Float>.size)
print(MemoryLayout<Float>.alignment)
```

出た、log

```
▿ simdFullTest.Light
  ▿ color: SIMD3<Float>(0.0, 0.0, 1.0)
    ▿ _storage: Swift.Float.SIMD4Storage
      - _value: (Opaque Value)
  - ambientIntensity: 0.5
light ---
32    //stride
20    // size
16    // alignment
float3 ---
16    // stride
16    // size
16    // alignment
Float ---
4   // stride
4   // size
4   // alignment
```



```
self	simdFullTest.ContentView	
  light	simdFullTest.Light	
    color	SIMD3<Float>	(0, 0, 1)	
      _storage	Float.SIMD4Storage	
        _value	Builtin.Vec4xFPIEEE32	
    ambientIntensity	Float	0b00111111000000000000000000000000
```

`float32` ということ。。。？

[1/11 数値計算(3), パターン認識(1)](https://lecture.ecc.u-tokyo.ac.jp/~ktanaka/is11/0111.html)
```
decode_float32(0b00111111000000000000000000000000)
=> 0.5
```

### float の値の変化

```
0.1
ambientIntensity	Float	0b00111101110011001100110011001101

0.2
ambientIntensity	Float	0b00111110010011001100110011001101

0.4
ambientIntensity	Float	0b00111110110011001100110011001101

0.5
ambientIntensity	Float	0b00111111000000000000000000000000

0.6
ambientIntensity	Float	0b00111111000110011001100110011010

0.9
ambientIntensity	Float	0b00111111011001100110011001100110

1.0
ambientIntensity	Float	0b00111111100000000000000000000000

```



## 📝 2021/11/27


どうもfloat のみ数値が通ってないようなきがする


## 📝 2021/11/23

### `node` の`modelMatrix`

`self.get_modelMatrix` とインスタンスメソッドで`modelMatrix` を呼び出していたが、要素のインスタンス変数変更後(`self.position` や`self.rotation` など) に、参照をする手立てがなかった


``` .py
class Node:
  def __init__(self):
    self.modelMatrix: 'matrix'
    self.position = float3(0.0, 0.0, 0.0)
    self.rotation = float3(0.0, 0.0, 0.0)
    self.scale = float3(1.0, 1.0, 1.0)
    self.modeMatrix = self.get_modelMatrix()

  def get_modelMatrix(self):
    matrix = matrix_float4x4.translation_x_y_z_(
      self.position.x, self.position.y, self.position.z)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.x, 1.0, 0.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.y, 0.0, 1.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.z, 0.0, 0.0, 1.0)
    matrix = matrix.scaledBy_x_y_z_(
      self.scale.x, self.scale.y, self.scale.z)
    return matrix

```

`modelMatrix` を`@property` として、要素のインスタンス変数変更後に、`modelMatrix` 参照をすると、要素のインスタンス変数の値を反映した情報を受け渡せるようにした


``` .py
class Node:
  def __init__(self):
    self.modelMatrix: 'matrix'
    self.position = float3(0.0, 0.0, 0.0)
    self.rotation = float3(0.0, 0.0, 0.0)
    self.scale = float3(1.0, 1.0, 1.0)

  @property
  def modelMatrix(self):
    return self.__get_modelMatrix()

  def __get_modelMatrix(self):
    matrix = matrix_float4x4.translation_x_y_z_(
      self.position.x, self.position.y, self.position.z)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.x, 1.0, 0.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.y, 0.0, 1.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.z, 0.0, 0.0, 1.0)
    matrix = matrix.scaledBy_x_y_z_(
      self.scale.x, self.scale.y, self.scale.z)
    return matrix

```
`instanceScene.py` で、要素を変更した際に、`node` の`add_childNode` 内を `render_commandEncoder_parentModelViewMatrix_` しなくても、`modelMatrix` の値更新ができるようになった


### このpyMetal のまとめ

現在も、構造として適宜変更が必要。解説として01 から書き始めた場合に、各章で色々なデータを書き直す必要が出てきそう。


最終章まで(いくことができれば) 終えることができた時に、再度コードを調整・整形をしつつ、整理として解説の記事を書いていくことですすめてみたいと思う


#### テストのドラフトの記事

テストとしてかんたんな記事化については、[pome-ta / draftPythonistaScripts](https://github.com/pome-ta/draftPythonistaScripts/blob/main/articles/metal/draft.md) に記載済み


画像や、図式での解説方法などは今後に考えておくことにする


### GitHub への`push`

[Working Copy](https://workingcopyapp.com/) では、[GitHub Desktop](https://desktop.github.com/) で`push` すると、アイコンが謎になるので

今回この`push` は、Terminal から実行してみる


他のリポジトリでは、気軽にbranch がうまく切れなかったりした。というのもあり



### PyCharm

インデントをスペース2つという、邪教の設定をして

コードの整形を一気におこなった



## 📝 2021/11/22

`newBufferWithLength` で生成した、Buffer をどうやってがっちゃんこして、格納するかが鍵


`Node` の`modelMatrix` が、想定挙動してくれないな、、、


## 📝 2021/11/17

### 画像取得を途中で割り込みすると読めなくなる

解決した😤


`renderable.py` 内で、`.metal`(シェーダーコード) を読み込む時に


``` .py
source = shader_path.read_text('utf-8')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
options = MTLCompileOptions.new()
library = device.newLibraryWithSource_options_error_(
      source, options, err_ptr)
```

と、`MTLCompileOptions.new()` option を入れることで解決


以前は、`err_ptr` (`= ctypes.c_void_p()`) をニュルッと差し込んでた。


エラーで、library の配列がどうたら（エラーログが見つからない）と怒られてたから

それをうまいように処理してくれてるのだと思う




## 📝 2021/11/16

### `texturable.py`

画像取得を途中で割り込みすると読めなくなる


### `renderable.py`

``` .py
source = shader_path.read_text('utf-8')

library = device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)
```


この読み込みが、同期で読んでるから？




## 📝 2021/11/15

swift の`do try` をPythonista(Python) `try` でキャッチできない問題


### `texturable` のエラー処理

texture データの`null` を返すオブジェクトを確認して

こちらで手動生成を試みる



## 📝 2021/11/14

### Swift 適当理解(間違いあり) まとめ

iOS Deploument Target: iOS 14.4

Swift Language Version: Swift 4


#### `!` と `?`

[Swift初心者向け ?と!の意味](https://qiita.com/Keech/items/2d3824091a83d2c205d3)


とりあえず、`?` をつけて、指摘があった部分を`fix` のやつで、なんとか逃げる



もしかしたら、ここらへんの雑`fix` が原因的なところがあるかもしれん



#### `at:` -> `index:`

言われるがままに`fix` を連打


#### `if #available(iOS 10.0, *)`

`if` での分岐を排除し、

##### 変更前


``` before.swift
    let textureLoader = MTKTextureLoader(device: device)
    var texture: MTLTexture? = nil
    let textureLoaderOptions: [String: NSObject]
    if #available(iOS 10.0, *) {
      let origin = NSString(string: MTKTextureLoaderOriginBottomLeft)
      textureLoaderOptions = [MTKTextureLoaderOptionOrigin : origin]
    } else {
      textureLoaderOptions = [:]
    }
```

##### 変更後

``` after.swift
    let textureLoader = MTKTextureLoader(device: device)
    var texture: MTLTexture? = nil
//    let textureLoaderOptions: [String: NSObject]
    let origin = NSString(string: MTKTextureLoader.Origin.bottomLeft.rawValue)
    let textureLoaderOptions = [MTKTextureLoader.Option.origin : origin]
```

#### `Type of expression is ambiguous without more context` のエラー


[Swift MetalKit unknknown return type MTKMesh.newMeshes](https://stackoverflow.com/questions/50224108/swift-metalkit-unknknown-return-type-mtkmesh-newmeshes)

[参照先: Writing a Modern Metal App from Scratch: Part 1](https://metalbyexample.com/modern-metal-1/)

このやつ

``` .swift
do {
      meshes = try MTKMesh.newMeshes(from: asset,
                                     device: device,
                                     sourceMeshes: nil)
    } catch {
      print("mesh error")
    }
```


事前に用意するものを変更して

``` .swift
var meshes: [MTKMesh] = []
```

こんな感じで呼び出す？

``` .swift
    do {
      (_, meshes) = try MTKMesh.newMeshes(asset: asset,
                                     device: device)
    } catch {
      print("mesh error")
    }
```

#### `Thread 1: signal SIGABRT` のエラー

多分Storyboard が明確に設定されていない？

過去の動くものまで、戻して違いを確認するしかなさそう。。。





## 📝 2021/11/13

texture がうまく反映されんのよな

変な形状での描画はできたけど、色々と確認する部分は多い。。。

### `MDLAsset`

しれっと、何かしらの巻き添いで、呼べてたが

~~ 本来は、`load_framework('ModelIO')` が必要 ~~

↑ 違う、巻き添い呼び出しで問題なさそう



### Obj ファイル


検証用、確認用ファイルの参照先

[9. Model I/O: `mushroom`](https://www.raywenderlich.com/3537-beginning-metal/lessons/9)


[29. Textures: `train`](https://www.raywenderlich.com/1258241-3d-graphics-with-metal/lessons/29)


参考サイト: [Objファイル基礎](https://yttm-work.jp/model_render/model_render_0001.html)


- `.obj`
  - 頂点
  - 法線

- `.mtl`
  - モデル色
  - テクスチャ

`.mtl` がなくても、`.obj` があればモデル形状を描画が可能


### 参照Log

とりあえず走るものとして、


[29. Textures: `train`](https://www.raywenderlich.com/1258241-3d-graphics-with-metal/lessons/29)


`MDLVertexAttributePosition` = `position`


`MDLVertexAttributeNormal` = `normal`



などなど、突っ込んだらそれなりな通常な変数にになるかも

```
vertexDescriptor ---
<MDLVertexDescriptor: 0x60000024b460 attributes:(
    "<MDLVertexAttribute: 0x60000175d9c0 name=position format=Float3 bufferIndex=0 offset=0>",
    "<MDLVertexAttribute: 0x60000175da40 name=normal format=Float3 bufferIndex=0 offset=16>",
    "<MDLVertexAttribute: 0x60000175da80 name=textureCoordinate format=Float2 bufferIndex=0 offset=32>"
) layouts:{
    0 = "<MDLVertexBufferLayout: 0x600000011030 stride=40>";
}>
vertexDescriptor ---
<MDLVertexDescriptor: 0x600000254ec0 attributes:(
    "<MDLVertexAttribute: 0x60000174b840 name=position format=Float3 bufferIndex=0 offset=0>",
    "<MDLVertexAttribute: 0x60000174b1c0 name=normal format=Float3 bufferIndex=0 offset=16>",
    "<MDLVertexAttribute: 0x60000174b200 name=textureCoordinate format=Float2 bufferIndex=0 offset=32>"
) layouts:{
    0 = "<MDLVertexBufferLayout: 0x600000008dc0 stride=40>";
}>
```



### MTLVertexDescriptor

```
MTLVertexDescriptor ---
- <MTLVertexDescriptorInternal: 0x600000255440>
    Buffer 0:
        stepFunction = MTLVertexStepFunctionPerVertex
        stride = 40
        Attribute 0:
            offset = 0
            format = MTLAttributeFormatFloat3
        Attribute 1:
            offset = 16
            format = MTLAttributeFormatFloat3
        Attribute 2:
            offset = 32
            format = MTLAttributeFormatFloat2 #0
  - super: MTLVertexDescriptor
    - super: NSObject
    --- --- ---
```

### MDLVertexDescriptor


```
MDLVertexDescriptor ---
- <MDLVertexDescriptor: 0x600000258560 attributes:(
    "<MDLVertexAttribute: 0x600001767280 name=position format=Float3 bufferIndex=0 offset=0>",
    "<MDLVertexAttribute: 0x600001767300 name=normal format=Float3 bufferIndex=0 offset=16>",
    "<MDLVertexAttribute: 0x600001767340 name=textureCoordinate format=Float2 bufferIndex=0 offset=32>"
) layouts:{
    0 = "<MDLVertexBufferLayout: 0x600000004c90 stride=40>";
}> #0
  - super: NSObject
    --- --- ---
```


#### 全体

```
MTLVertexDescriptor ---
- <MTLVertexDescriptorInternal: 0x600000255440>
    Buffer 0:
        stepFunction = MTLVertexStepFunctionPerVertex
        stride = 40
        Attribute 0:
            offset = 0
            format = MTLAttributeFormatFloat3
        Attribute 1:
            offset = 16
            format = MTLAttributeFormatFloat3
        Attribute 2:
            offset = 32
            format = MTLAttributeFormatFloat2 #0
  - super: MTLVertexDescriptor
    - super: NSObject
    --- --- ---
MTLVertexDescriptor ---
- <MTLVertexDescriptorInternal: 0x6000002584a0>
    Buffer 0:
        stepFunction = MTLVertexStepFunctionPerVertex
        stride = 40
        Attribute 0:
            offset = 0
            format = MTLAttributeFormatFloat3
        Attribute 1:
            offset = 16
            format = MTLAttributeFormatFloat3
        Attribute 2:
            offset = 32
            format = MTLAttributeFormatFloat2 #0
  - super: MTLVertexDescriptor
    - super: NSObject
    --- --- ---
MDLVertexDescriptor ---
- <MDLVertexDescriptor: 0x600000258560 attributes:(
    "<MDLVertexAttribute: 0x600001767280 name=position format=Float3 bufferIndex=0 offset=0>",
    "<MDLVertexAttribute: 0x600001767300 name=normal format=Float3 bufferIndex=0 offset=16>",
    "<MDLVertexAttribute: 0x600001767340 name=textureCoordinate format=Float2 bufferIndex=0 offset=32>"
) layouts:{
    0 = "<MDLVertexBufferLayout: 0x600000004c90 stride=40>";
}> #0
  - super: NSObject
    --- --- ---
MTLVertexDescriptor ---
- <MTLVertexDescriptorInternal: 0x600000258560>
    Buffer 0:
        stepFunction = MTLVertexStepFunctionPerVertex
        stride = 40
        Attribute 0:
            offset = 0
            format = MTLAttributeFormatFloat3
        Attribute 1:
            offset = 16
            format = MTLAttributeFormatFloat3
        Attribute 2:
            offset = 32
            format = MTLAttributeFormatFloat2 #0
  - super: MTLVertexDescriptor
    - super: NSObject
    --- --- ---
MDLVertexDescriptor ---
- <MDLVertexDescriptor: 0x600000258500 attributes:(
    "<MDLVertexAttribute: 0x60000176c340 name=position format=Float3 bufferIndex=0 offset=0>",
    "<MDLVertexAttribute: 0x60000176c380 name=normal format=Float3 bufferIndex=0 offset=16>",
    "<MDLVertexAttribute: 0x60000176c3c0 name=textureCoordinate format=Float2 bufferIndex=0 offset=32>"
) layouts:{
    0 = "<MDLVertexBufferLayout: 0x600000004ae0 stride=40>";
}> #0
  - super: NSObject
    --- --- ---
```


## 📝 2021/10/05


obj を読んでエクスポートすると、足りない情報ありそう

先によみこんだりするのか？



`Bundle = ObjCClass('NSBundle')`

でbundle に突っ込んでみる作戦


## 📝 2021/10/04


`MDLVertexAttributePosition` あたりのを`position` で読む感じになってる


ずっと **Metal I/O** だと思ってたら **Model I/O** だった😇


何にせよ呼び出せない、、、





## 📝 2021/09/30

違うサンプルで、mesh 読み込みの仕組みをみる





## 📝 2021/09/25

描画できない理由を探るのが難しいな



## 📝 2021/09/23


`objectAtIndexedSubscript_` ? `objectAtIndex`





## 📝 2021/09/21

`MTKModelIOVertexDescriptorFromMetal` らへんの呼び出しな面倒




## 📝 2021/09/19

camera で試行錯誤をしてきたが


一度コードを整理してみる


### 座標系

- Metal, DirectX
  - 左手座標系

OpenGL, WebGL
  - 右手座標系


### マシンログ出し

- gameScene
  - scale なしと、指定の時

そもそも、Shader のコードが違ってた

本機で試してみたところ、端末により描画が違ってた


## 📝 2021/09/14

### 原因

`node` の`self.modelMatrix` が値更新されてなかった


毎回読み直す処理にしたけど、もう少し手軽にできんかな？

## 📝 2021/09/13

全然呼び出せない

### 実行の順番の整理

- `view`
  - `GameScene`
    - `Plane`
      - ひとつづつの書き出しやる
  - `Renderer` に、`GameScene` 入れる


### 書き換え

クソでかclass になってないか？




## 📝 2021/09/12

差分という卑怯な手を使う

### gameScene

``` .swift
let quad2 = Plane(device: device,
imageName: "picture.png")
quad2.scale = float3(0.5)
quad2.position.y = 1.5
quad.add(childNode: quad2)
  }
override func update(deltaTime: Float) {
quad.rotation.y += deltaTime
}

```

### Node

``` .swift
var position = float3(0)
var rotation = float3(0)
var scale = float3(1)
var modelMatrix: matrix_float4x4 {
var matrix = matrix_float4x4(translationX: position.x,
y: position.y, z: position.z)
matrix = matrix.rotatedBy(rotationAngle: rotation.x,
x: 1, y: 0, z: 0)
matrix = matrix.rotatedBy(rotationAngle: rotation.y,
x: 0, y: 1, z: 0)
matrix = matrix.rotatedBy(rotationAngle: rotation.z,
x: 0, y: 0, z: 1)
matrix = matrix.scaledBy(x: scale.x, y: scale.y, z: scale.z)
return matrix
}

```

``` .swift
parentModelViewMatrix: matrix_float4x4) {
for child in children {	let modelViewMatrix = matrix_multiply(parentModelViewMatrix,
modelMatrix)


parentModelViewMatrix: modelViewMatrix)
}
if let renderable = self as? Renderable {
commandEncoder.pushDebugGroup(name)
renderable.doRender(commandEncoder: commandEncoder,
modelViewMatrix: modelViewMatrix)
commandEncoder.popDebugGroup()


```
### Plane

``` .swift
extension Plane: Renderable {
func doRender(commandEncoder: MTLRenderCommandEncoder, modelViewMatrix: matrix_float4x4) {
```


### Renderable

``` .swift
var modelConstants: ModelConstants { get set }
func doRender(commandEncoder: MTLRenderCommandEncoder,
modelViewMatrix: matrix_float4x4)
}	}
```

### Scene

``` .swift
func update(deltaTime: Float) {}
func render(commandEncoder: MTLRenderCommandEncoder,
deltaTime: Float) {
update(deltaTime: deltaTime)
let viewMatrix = matrix_float4x4(translationX: 0, y: 0, z: -4)
for child in children {
child.render(commandEncoder: commandEncoder,
parentModelViewMatrix: viewMatrix)
}
}
```



## 📝 2021/09/10

[OpenGLES-Pythonista](https://github.com/Cethric/OpenGLES-Pythonista) は偉大😭


まるっと、行列計算お借りした

### モジュール

`ctypes` で呼んでるものたちを分けるか？






## 📝 2021/09/09

### gl で作ったやつ

```
GLKMatrix4 {
{2.439, -0.764, 0.000, 0.000}
{1.359, 1.371, 0.000, 0.000}
{0.000, 0.000, -1.001, -1.000}
{0.000, 0.000, 3.904, 4.000}
}
```
勝った🎉


### numpy


ん？ matrix の私の考え方が間違えているのか

行列の計算だと期待結果が出ないんだが。。。


テストで喰わせた結果で一番近そうなのが


```.py
import numpy as np


projectionMatrix = np.array([
  [2.7919474, 0.0, 0.0, 0.0],
  [0.0, 1.5696856, 0.0, 0.0],
  [0.0, 0.0, -1.001001, -1.0],
  [0.0, 0.0, -0.1001001, 0.0]])

modelViewMatrix = np.array([
  [0.8735571, -0.48672166, 0.0, 0.0],
  [0.48672166, 0.8735571, 0.0, 0.0],
  [0.0, 0.0, 1.0, 0.0],
  [0.0, 0.0, -4.0, 1.0]])


matrix_multiply = np.dot(projectionMatrix, modelViewMatrix)
'''
[[ 2.43892547 -1.35890127  0.          0.        ]
 [ 0.76399998  1.37121     0.          0.        ]
 [ 0.          0.          2.998999   -1.        ]
 [ 0.          0.         -0.1001001   0.        ]]
'''

matrix_multiply = projectionMatrix * modelViewMatrix
'''
[[ 2.43892547 -0.          0.          0.        ]
 [ 0.          1.37121     0.          0.        ]
 [ 0.          0.         -1.001001   -0.        ]
 [ 0.          0.          0.4004004   0.        ]]
'''

matrix_multiply = np.multiply(projectionMatrix, modelViewMatrix)
'''
[[ 2.43892547 -0.          0.          0.        ]
 [ 0.          1.37121     0.          0.        ]
 [ 0.          0.         -1.001001   -0.        ]
 [ 0.          0.          0.4004004   0.        ]]
'''


```


## 📝 2021/09/08


```
rotationMatrix ---
▿ simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8736 -0.4867  0.0000  0.0000"
  -  : " 0.4867  0.8736  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
viewMatrix ---
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
matrix_multiply ---
▿ simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8736 -0.4867  0.0000  0.0000"
  -  : " 0.4867  0.8736  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"

```


```
projectionMatrix ---
▿ simd_float4x4([[2.7919474, 0.0, 0.0, 0.0], [0.0, 1.5696856, 0.0, 0.0], [0.0, 0.0, -1.001001, -1.0], [0.0, 0.0, -0.1001001, 0.0]])
  -  : " 2.7919  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.5697  0.0000  0.0000"
  -  : " 0.0000  0.0000 -1.0010 -1.0000"
  -  : " 0.0000  0.0000 -0.1001  0.0000"
modelViewMatrix ---
▿ simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8736 -0.4867  0.0000  0.0000"
  -  : " 0.4867  0.8736  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
matrix_multiply ---
▿ simd_float4x4([[2.4389255, -0.764, 0.0, 0.0], [1.3589013, 1.37121, 0.0, 0.0], [0.0, 0.0, -1.001001, -1.0], [0.0, 0.0, 3.903904, 4.0]])
  -  : " 2.4389 -0.7640  0.0000  0.0000"
  -  : " 1.3589  1.3712  0.0000  0.0000"
  -  : " 0.0000  0.0000 -1.0010 -1.0000"
  -  : " 0.0000  0.0000  3.9039  4.0000"

```




`animateBy` の数値をとらないけないから

06 に戻り、時間を取得

```
|animateBy         |time              |
|------------------|------------------|
|0.5083329475362225|0.0166666666666667|
|0.5166635804183768|0.0333333333333333|
|0.5249895846353392|0.0500000000000000|
|0.5333086474616965|0.0666666666666667|

~ 中略 ~

|0.9987527233157389|7.7833333333333110|
|0.9992716726873019|7.7999999999999776|
|0.9996519386934261|7.8166666666666442|
|0.9998934157071104|7.8333333333333108|
|0.9999960366529593|7.8499999999999774| * top
|0.9999597730258144|7.8666666666666440|
|0.9997846348986723|7.8833333333333107|
|0.9994706709198866|7.8999999999999773|
|0.9990179682996547|7.9166666666666439|

~ 中略 ~

|0.0009681714824467|10.9333333333334561|
|0.0005191640530888|10.9500000000001236|
|0.0002088980887302|10.9666666666667911|
|0.0000374597723661|10.9833333333334586|
|0.0000048967246485|11.0000000000001261| * bottom
|0.0001112179906593|11.0166666666667936|
|0.0003563940373971|11.0333333333334611|
|0.0007403567619808|11.0500000000001286|
|0.0012629995105669|11.0666666666667961|

```

## 📝 2021/09/07

恒例のlog check ⏰

### Swift のバージョン違い


sample が、3.0 みたいで、4.0 以上にせないけんし

iOS も、面倒回避でバージョン調整をした


調整とはいえ、エラーに対して`fix` をポチーして、それでダメなら無理矢理インスタンスを作る作戦


matrix の`print` やら、`dump` やら

```.swift
    let rotationMatrix = matrix_float4x4(rotationAngle: animateBy,
                                         x: 0, y: 0, z: 1)
```

```
simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8736 -0.4867  0.0000  0.0000"
  -  : " 0.4867  0.8736  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.86947215, -0.49398196, 0.0, 0.0], [0.49398196, 0.86947215, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[0.86947215, -0.49398196, 0.0, 0.0], [0.49398196, 0.86947215, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8695 -0.4940  0.0000  0.0000"
  -  : " 0.4940  0.8695  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.86532915, -0.501204, 0.0, 0.0], [0.501204, 0.86532915, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[0.86532915, -0.501204, 0.0, 0.0], [0.501204, 0.86532915, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8653 -0.5012  0.0000  0.0000"
  -  : " 0.5012  0.8653  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.8611297, -0.5083853, 0.0, 0.0], [0.5083853, 0.8611297, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[0.8611297, -0.5083853, 0.0, 0.0], [0.5083853, 0.8611297, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8611 -0.5084  0.0000  0.0000"
  -  : " 0.5084  0.8611  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.8568754, -0.5155235, 0.0, 0.0], [0.5155235, 0.8568754, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[0.8568754, -0.5155235, 0.0, 0.0], [0.5155235, 0.8568754, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.8569 -0.5155  0.0000  0.0000"
  -  : " 0.5155  0.8569  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.8525681, -0.5226162, 0.0, 0.0], [0.5226162, 0.8525681, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
```



```.swift
    let viewMatrix = matrix_float4x4(translationX: 0, y: 0, z: -4)
```

```
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
```

```.swift
    let modelViewMatrix = matrix_multiply(rotationMatrix, viewMatrix)
```

```
simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.8735571, -0.48672166, 0.0, 0.0], [0.48672166, 0.8735571, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8736 -0.4867  0.0000  0.0000"
  -  : " 0.4867  0.8736  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.86947215, -0.49398196, 0.0, 0.0], [0.49398196, 0.86947215, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.86947215, -0.49398196, 0.0, 0.0], [0.49398196, 0.86947215, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8695 -0.4940  0.0000  0.0000"
  -  : " 0.4940  0.8695  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.86532915, -0.501204, 0.0, 0.0], [0.501204, 0.86532915, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.86532915, -0.501204, 0.0, 0.0], [0.501204, 0.86532915, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8653 -0.5012  0.0000  0.0000"
  -  : " 0.5012  0.8653  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.8611297, -0.5083853, 0.0, 0.0], [0.5083853, 0.8611297, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.8611297, -0.5083853, 0.0, 0.0], [0.5083853, 0.8611297, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8611 -0.5084  0.0000  0.0000"
  -  : " 0.5084  0.8611  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.8568754, -0.5155235, 0.0, 0.0], [0.5155235, 0.8568754, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.8568754, -0.5155235, 0.0, 0.0], [0.5155235, 0.8568754, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8569 -0.5155  0.0000  0.0000"
  -  : " 0.5155  0.8569  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.8525681, -0.5226162, 0.0, 0.0], [0.5226162, 0.8525681, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
▿ simd_float4x4([[0.8525681, -0.5226162, 0.0, 0.0], [0.5226162, 0.8525681, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
  -  : " 0.8526 -0.5226  0.0000  0.0000"
  -  : " 0.5226  0.8526  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  0.0000 -4.0000  1.0000"
simd_float4x4([[0.8482093, -0.5296612, 0.0, 0.0], [0.5296612, 0.8482093, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, -4.0, 1.0]])
```

### Challenge の方だけど

なぜか、スケールだけ取れる

```.swift
  func scaledBy(x: Float, y: Float, z: Float) -> matrix_float4x4 {
    let scaledMatrix = matrix_float4x4(scaleX: x, y: y, z: z)
    dump(self)
    print(self)
    return matrix_multiply(self, scaledMatrix)
  }

```


同じのが、飛んでいっているかな？

```
▿ simd_float4x4([[0.9998611, 0.0, 0.016665896, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.016665896, 0.0, 0.9998611, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9999  0.0000  0.0167  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0167  0.0000  0.9999  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9998611, 0.0, 0.016665896, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.016665896, 0.0, 0.9998611, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.9994445, 0.0, 0.033327162, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.033327162, 0.0, 0.9994445, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9994  0.0000  0.0333  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0333  0.0000  0.9994  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9994445, 0.0, 0.033327162, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.033327162, 0.0, 0.9994445, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.99875027, 0.0, 0.049979173, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.049979173, 0.0, 0.99875027, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9988  0.0000  0.0500  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0500  0.0000  0.9988  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.99875027, 0.0, 0.049979173, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.049979173, 0.0, 0.99875027, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"

```

```
self	simd_float4x4	\n[ [5.948225e-01, 0.000000e+00, -8.038571e-01, 0.000000e+00],\n  [0.000000e+00, 1.000000e+00, 0.000000e+00, 0.000000e+00],\n  [8.038571e-01, 0.000000e+00, 5.948225e-01, 0.000000e+00],\n  [0.000000e+00, 0.000000e+00, 0.000000e+00, 1.000000e+00] ]\n
```

### ディレクトリ構造

Pythonista と xcode だと見え方違う？


- Nodes
  - Node
  - Plane
  - Renderable
  - Texurable

- Scenes
  - Scene
  - GameScene


## 📝 2021/09/05

swift やobjective-c の構造体や関数。それでいて、swift の`extension` など


無駄に頭で考えてしまって、進捗が悪い


クラスメソッドでいくのだろうけど、、、？


### `ctypes`

- 構造体 (`Structure`)
- 共用体 (`Union`)


型が同じであれば構造体、違う型でつくるなら共用体


初期の数値ってどうなるのだろうか？と小一時間




## 📝 2021/09/04

matrix 実装がめんどいよぉ、、、


## 📝 2021/09/02


7 のMatrices に入るにあたり、計算ゴリゴリ書きそうだったので、一時休止



### 6 のTexture 関係

呼び出しや、mask は完了

#### `texture` を2種類ほど呼び出し

mask をするにあたり、ベースの`texture` の時にはmask を呼び出さない事もあり、そのハンドリングに悩んでいたが


`Plane` の`__init__` に、先に定義することで解決

``` .py
self.texture = None
self.maskTexture = None
```


#### `__init__` の定義と、class変数


見本コードでは、`init` 外の定義も`__init__` で定義させている

色々調べるに、class変数には、あまりメリットなし？な印象があるので

インスタンス変数として、処理していることになる


この書き方で、ええのだろうか？


### モジュールわけわけ

7 のMatrices 前にモジュールを分けてしまおうという魂胆



[[初心者向け] Pythonのパッケージを自作して、パッケージとモジュールへの理解を深めてみる](https://dev.classmethod.jp/articles/python-create-package/)

[Python命名規則一覧](https://qiita.com/naomi7325/items/4eb1d2a40277361e898b)



`__init__.py` 内の定義とか、ファイル名にドキドキしながら

実装ちう


`objc_util` モジュールを書きまくりそうだから調べたら、ダメって書いてあった


[自作パッケージ配下の各モジュールに同じモジュールを一括でインポートしたい。](https://teratail.com/questions/217084)





## 📝 2021/08/29

beginningMetal もTexture の章となり、いつもの実装とは違う難しさがでてきた


通常(?) のiOS 開発であると、`Assets` に必要なものをガバっと入れて、ゴリッと呼び出すのであろうが(実際そうであるかは知らん)

Pythonista では、`path` 定義をしたり、データなのか`URL` なのか？みたいなことなど、自動的に処理してくれそうな部分のケアまで必要であったり(実際がそうであるかは知らん)


サンプルコードを丸写しで実行完了ができないので、面倒な部分ではある


Pythonista でやっている以上、それが必要な作業であると理解をしているが
どうも、画像処理となると自分の興味のフィールドから少し離れてしまうので
重い腰となってしまうことがある


## 📝 2021/08/24

[mtlvertexformat](https://developer.apple.com/documentation/metal/mtlvertexformat)


`.float3` って`ctypes` のでいいのかな、、、


まぁ動いてるからヨシ





問題なく描画した後に、ちょっと書き換えて実行すると落ちるなぁ


## 📝 2021/08/23

恒例ログ取り


`swift` サンプルコードの数値確認


``` .swift
// 16
print(MemoryLayout<float3>.stride)

// float2 = 8
// float3 = 16
// float4 = 16

dump(MemoryLayout<float2>.size) //  8
dump(MemoryLayout<float3>.size) //  16
dump(MemoryLayout<float4>.size) //  16

// 32
print(MemoryLayout<Vertex>.stride)
// .size => 32




print(vertices.count)   // 4
    print(MemoryLayout<Vertex>.stride)  //32
    print(vertices.count *
            MemoryLayout<Vertex>.stride)  // 128
```


## 📝 2021/08/21

サンプルコードに寄せ、コードの構造を変えている

`objc_util` が、エラー = 即落ちなので


なかなか、ログが取れずかなり時間を溶かした


落ちる瞬間に、エラーのウィンドウが出れば、携帯で動画キャプチャをして、一時停止しながらエラーメッセージを読む（ウィンドウが出ればの話）


Python 側のエラーでもマルっと落ちてしまうのがネック


### 今回の凡ミス

``` .py
class Plane(Node):
  def __init__(self, device):
    super().__init__()
    self.vertices = (ctypes.c_float * 12)(
      -1.0,  1.0, 0.0,    # v0
      -1.0, -1.0, 0.0,    # v1
       1.0, -1.0, 0.0,    # v2
       1.0,  1.0, 0.0,)   # v3
    # 色々処理
    self.buildBuffers(device)

  def buildBuffers(self, device):
    self.vertexBuffer = device.newBufferWithBytes_length_options_(
      self.vertices, self.vertices.__len__() * ctypes.sizeof(self.vertices), 0)
    # 色々処理

  def render_commandEncoder_deltaTime_(commandEncoder, deltaTime):
  # ↑ `self` 抜けてる
    super().render_commandEncoder_deltaTime_(commandEncoder, deltaTime)

    self.time += deltaTime
    animateBy = abs(sin(self.time) / 2 + 0.5)
    self.constants.animateBy = animateBy

```


継承(`Node`) したクラスのオーバーライド時に、`Plane` クラスの関数引数に`self` を入れ忘れてた






## 📝 2021/08/18

### ディレクトリ整理

ディレクトリが散漫しすぎて、ひどいけど`_old` を作ってぶち込んだ



### beginning metal シリーズ！


`setVertexBytes_` 問題がどうにもならず

適当にYoutube 見てたら、御用達サイトの一つ[raywenderlich.com](https://www.raywenderlich.com/) のチャンネルを見つけた


[Beginning Metal](https://www.raywenderlich.com/3537-beginning-metal) の[YouTube 動画](https://youtu.be/Gqj2lP7qlAM) (Part が散らかってるので探すのがめんどう) は見れた & iOS8 swift3 のプロジェクトであったらダウンロードができたので


再度一から入門としてやってみる






## 📝 2021/08/14


`setVertexBytes_length_atIndex_` と`setVertexBuffer_offset_atIndex_`


`setVertexBytes_` がうまく渡せていない？





## 📝 2021/08/13

[Using a Render Pipeline to Render Primitives](https://developer.apple.com/documentation/metal/using_a_render_pipeline_to_render_primitives?language=objc) の、`AAPLShaderTypes.h` 扱い問題


そもそも、何かしらの呼び出しがだめかもしれん

うまいログだし方法を考えないといけない




## 📝 2021/08/08


[Moving from OpenGL to Metal | raywenderlich.com](https://www.raywenderlich.com/9211-moving-from-opengl-to-metal)



これを、[移植してみた](https://github.com/pome-ta/pystaMetalStudy/tree/main/src/matrix/GLKitMath)



GLKit のmatrix 計算をまるっと


[OpenGLES-Pythonista | Cethric](https://github.com/Cethric/OpenGLES-Pythonista)


お借りしたけど、3系とかにいつか書き換えたいねー


## 📝 2021/08/07


頂点のやつ


[MTLResourceOptions Enum](https://docs.microsoft.com/en-us/dotnet/api/metal.mtlresourceoptions?view=xamarin-ios-sdk-12)

これか？


## 📝 2021/08/05

### todo

ここのreadme.md を整理せな、、、



### viewのサイズ


`-(-float // float)` で小数点切り捨てしてるけど`int(float)` でよかった？




## 📝 2021/08/04


### ~~スレッドが一つしか走ってない？~~


呼び出すコードまちがえてますた 😇

``` .py
# 正解

dispatchThreadgroups_threadsPerThreadgroup_()
```


``` .py
# 間違え

dispatchThreads_threadsPerThreadgroup_()
```

しかし、そうなると、画面サイズ変わるん？


割り算で`int` するし、、、





[【Swift Metal】dispatchThreadgroupsの最適化ついて解説](https://hirauchi-genta.com/swift-metal-dispatchthreadgroups/)

[【Swift Metal】thread_position_in_grid等の属性について解説](https://hirauchi-genta.com/swift-metal-attribute/)


### Shader 拡張子


Pythonista で毎回見づらいから、`.js` にした


普通に動いてるぽから、よかった




## 📝 2021/08/03


### translationMatrix

```
translationMatrix simd_float4x4(
  [[1.0, 0.0, 0.0, 0.0],
  [0.0, 1.0, 0.0, 0.0],
  [0.0, 0.0, 1.0, 0.0],
  [0.0, 0.0, -3.0, 1.0]]
)
```

### scalingMatrix

```
scalingMatrix simd_float4x4(
  [[0.5, 0.0, 0.0, 0.0],
  [0.0, 0.5, 0.0, 0.0],
  [0.0, 0.0, 0.5, 0.0],
  [0.0, 0.0, 0.0, 1.0]]
)
```

### rotationMatrix

```
rotationMatrix simd_float4x4(
  [[1.0, 0.0, 0.0, 0.0],
  [0.0, 0.7071068, -0.70710677, 0.0],
  [0.0, 0.70710677, 0.7071068, 0.0],
  [0.0, 0.0, 0.0, 1.0]]
)
```

### projectionMatrix

```
projectionMatrix simd_float4x4(
  [[1.8304877, 0.0, 0.0, 0.0],
  [0.0, 1.8304877, 0.0, 0.0],
  [0.0, 0.0, -1.0, -1.0],
  [0.0, 0.0, -0.0, 0.0]]
)
```


### size 関係

```
MemoryLayout<Vertex>.size * vertexData.count:  256
MemoryLayout<UInt16>.size * indexData.count:  72
MemoryLayout<matrix_float4x4>.size:  64
MemoryLayout<Uniforms>.size:  64
indexCount:  36
--- indexBuffer.length:  72
--- MemoryLayout<UInt16>.size:  2
```

```
# fastMathEnabled: true
    # 131075  version2_3
    # case version1_0 = 65536
    # case version1_1 = 65537
    # case version1_2 = 65538
    # case version2_0 = 131072
    # case version2_1 = 131073
    # case version2_2 = 131074
    # case version2_4 = 131076
```


## 📝 2021/08/02

```
>>> import numpy as np
>>> np.__version__
'1.8.0'

```


matrix が雰囲気により、描画がガバガバである😇



## 📝 2021/07/31


ndarray <-> ctypes で進めてるけど

変数作るところ(？) で、値が変わる

## 📝 2021/07/29

### 教訓

`int` は`int` で入れる😡


特に除算は、`float` になるで、Python に毒されすぎ(言い過ぎ、自分の凡ミス)


## 📝 2021/07/28

### matrix

コードの記述はできた。view が正方形でないので三角形が歪だが、スクエアのview だと見本と同じになってる

### メモリコピー

`memcpy` ここの流れを脳を殺し、`Vertex` と同様の投げ方をしてる





## 📝 2021/07/27

構造体の作りを、ただの配列にした


`ctypes.byref(vertexData)` と呼ばずに直で呼び出せるけど、キモい関数作るデメリットしか感じられん😇


Numpy でガチャーっとできるのかしら？そっちの方が有益かもしらん




正直、ポインタ渡すとか意味わからんて、、、、



## 📝 2021/07/26

まーた、チュートリアルサイト参考先を変える


[このリポジトリ](https://github.com/MetalKit/metal)



> There are two ways we can prepare our class for drawing: either conform to the MTKViewDelegate protocol and implement its drawInView(:) method, or subclass MTKView and override its drawRect(:)method.


> We choose the latter, so go ahead and change the class type from NSView to MTKView, and create a new method named render() that has the following content:

> 後者(`drawRect(:)`)を選択するので、先に進んでクラスタイプをNSViewからMTKViewに変更し、次の内容を持つrender（）という名前の新しいメソッドを作成します。




override はキモいので、`MTKViewDelegate` から、`drawInView(:)` でやる


### お、、、

リポジトリと記事にズレあり？とりま、脳内補完で進む


metal 使ったkodelife やりたいなー



## 📝 2021/07/25

### 構造体からの`length` 確認 その2


> `ctypes.sizeof` で良さそう

よくない🙅‍♂️



#### (多分) `ctypes` の場合は

`ctypes.c_float` が`4` ぽい

指定の型を変えれば良きようになりそうだけど


(その数値が何を指してるか
は調べてない)


#### 原因

要素が4つあったので`4` で出したときに

4 * 4 = 16 スタートの

いい感じで`ctypes.sizeof` が、`length` の数値とマッチしたっぽい


要素が3だと出したいものが出せない

```
🙆‍♂️: 96 = (4 * 4) * (3 * 2)
```

```
🙅‍♂️: 48 = (4 * 3) * (4)
↑ 本当は`64` が欲しい
```







## 📝 2021/07/24

```
vertices Optional([MetalDay1.Vertex(position: SIMD3<Float>(-1.0, -1.0, 0.0)),
                   MetalDay1.Vertex(position: SIMD3<Float>(1.0, -1.0, 0.0)),
                   MetalDay1.Vertex(position: SIMD3<Float>(-1.0, 1.0, 0.0)),
                   MetalDay1.Vertex(position: SIMD3<Float>(1.0, 1.0, 0.0))])

▿ Optional([MetalDay1.Vertex(position: SIMD3<Float>(-1.0, -1.0, 0.0)),
            MetalDay1.Vertex(position: SIMD3<Float>(1.0, -1.0, 0.0)),
            MetalDay1.Vertex(position: SIMD3<Float>(-1.0, 1.0, 0.0)),
            MetalDay1.Vertex(position: SIMD3<Float>(1.0, 1.0, 0.0))])

  ▿ some: 4 elements
    ▿ MetalDay1.Vertex
      ▿ position: SIMD3<Float>(-1.0, -1.0, 0.0)
        ▿ _storage: Swift.Float.SIMD4Storage
          - _value: (Opaque Value)
    ▿ MetalDay1.Vertex
      ▿ position: SIMD3<Float>(1.0, -1.0, 0.0)
        ▿ _storage: Swift.Float.SIMD4Storage
          - _value: (Opaque Value)
    ▿ MetalDay1.Vertex
      ▿ position: SIMD3<Float>(-1.0, 1.0, 0.0)
        ▿ _storage: Swift.Float.SIMD4Storage
          - _value: (Opaque Value)
    ▿ MetalDay1.Vertex
      ▿ position: SIMD3<Float>(1.0, 1.0, 0.0)
        ▿ _storage: Swift.Float.SIMD4Storage
          - _value: (Opaque Value)
---
indices Optional([0, 1, 2, 1, 2, 3])

▿ Optional([0, 1, 2, 1, 2, 3])
  ▿ some: 6 elements
    - 0
    - 1
    - 2
    - 1
    - 2
    - 3
```


実機でのプリントデバック


``` .swift
private func buildBuffer() {
    vertexBuffer = mtlDevice.makeBuffer(bytes: vertices, length: vertices.count*MemoryLayout<Vertex>.stride, options: [])
    indexBuffer = mtlDevice.makeBuffer(bytes: indices, length: indices.count*MemoryLayout<UInt16>.stride, options: [])

    print("vertexBuffer", vertices.count*MemoryLayout<Vertex>.stride)
    //  64

    print("indexBuffer", indices.count*MemoryLayout<UInt16>.stride)
    //  12
}

```

``` .swift
commandEncoder?.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
commandEncoder?.setVertexBytes(&uniforms, length: MemoryLayout<Uniforms>.stride, index: 1)
print("Uniforms", MemoryLayout<Uniforms>.stride)
//  16
commandEncoder?.drawIndexedPrimitives(type: .triangle, indexCount: indices.count, indexType: .uint16, indexBuffer: indexBuffer, indexBufferOffset: 0)
print("indices.count", indices.count)
// 6

```



## 📝 2021/07/23


参照コードが点在しすぎだから、そろそろ調整していかないと


### 構造体からの`length` 確認

[Using a Render Pipeline to Render Primitives](https://developer.apple.com/documentation/metal/using_a_render_pipeline_to_render_primitives?language=objc) のコード


``` objc
// Pass in the parameter data.
NSLog(@"triangleVertices %lu", sizeof(triangleVertices));
//  96
[renderEncoder setVertexBytes:triangleVertices
                       length:sizeof(triangleVertices)
                      atIndex:AAPLVertexInputIndexVertices];

NSLog(@"_viewportSize %lu", sizeof(_viewportSize));
//  8
[renderEncoder setVertexBytes:&_viewportSize
                       length:sizeof(_viewportSize)
                      atIndex:AAPLVertexInputIndexViewportSize];
```




あと、過去のswift で取得した参照のLog とり

``` .swift
vertices.count
//  3

MemoryLayout<Vertex>.stride
//  32

length = vertices.count * MemoryLayout<Vertex>.stride
//96

```

``` .python
class Position(ctypes.Structure):
  _fields_ = [('x', ctypes.c_float), ('y', ctypes.c_float),
              ('z', ctypes.c_float), ('w', ctypes.c_float)]


class Color(ctypes.Structure):
  _fields_ = [('r', ctypes.c_float), ('g', ctypes.c_float),
              ('b', ctypes.c_float), ('a', ctypes.c_float)]


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color)]


class PyVertex(ctypes.Structure):
  _fields_ = [('x', Vertex), ('y', Vertex), ('z', Vertex)]


vertexData = PyVertex(
  Vertex(Position(-0.8, -0.8,  0.0,  1.0), Color(1.0, 0.0, 0.0, 1.0)),
  Vertex(Position( 0.8, -0.8,  0.0,  1.0), Color(0.0, 1.0, 0.0, 1.0)),
  Vertex(Position( 0.0,  0.8,  0.0,  1.0), Color(0.0, 0.0, 1.0, 1.0)))


dataSize = ctypes.sizeof(vertexData)
# 96
```

`ctypes.sizeof` で良さそう



## 📝 2021/07/21

サイズの取得があやしい

Swift で確認の必要あり？





## 📝 2021/07/20

- 色々と参照したサイトの書き方がmix されてるから、整理したい
- class の書くところがバラバラだから、うまく調整したい


## 📝 2021/07/19

実際のSwift 実行での、状況確認


頂点の構造体指定の部分

``` .swift
let vertices = [Vertex(color: [1, 0, 0, 1], pos: [-1, -1]),
                Vertex(color: [0, 1, 0, 1], pos: [0, 1]),
                Vertex(color: [0, 0, 1, 1], pos: [1, -1])]
```

### log

以下、状況で取得し吐き出し


- `dump` でなんか色々と出力するやつ

``` .swift
dump(vertices)
```

```
▿ 3 elements
  ▿ __C.Vertex
    ▿ color: SIMD4<Float>(1.0, 0.0, 0.0, 1.0)
      ▿ _storage: Swift.Float.SIMD4Storage
        - _value: (Opaque Value)
    ▿ pos: SIMD2<Float>(-1.0, -1.0)
      ▿ _storage: Swift.Float.SIMD2Storage
        - _value: (Opaque Value)
  ▿ __C.Vertex
    ▿ color: SIMD4<Float>(0.0, 1.0, 0.0, 1.0)
      ▿ _storage: Swift.Float.SIMD4Storage
        - _value: (Opaque Value)
    ▿ pos: SIMD2<Float>(0.0, 1.0)
      ▿ _storage: Swift.Float.SIMD2Storage
        - _value: (Opaque Value)
  ▿ __C.Vertex
    ▿ color: SIMD4<Float>(0.0, 0.0, 1.0, 1.0)
      ▿ _storage: Swift.Float.SIMD4Storage
        - _value: (Opaque Value)
    ▿ pos: SIMD2<Float>(1.0, -1.0)
      ▿ _storage: Swift.Float.SIMD2Storage
        - _value: (Opaque Value)
```



- `print` でざっくり吐き出し

``` .swift
print(vertices)
```


```
[__C.Vertex(color: SIMD4<Float>(1.0, 0.0, 0.0, 1.0), pos: SIMD2<Float>(-1.0, -1.0)), __C.Vertex(color: SIMD4<Float>(0.0, 1.0, 0.0, 1.0), pos: SIMD2<Float>(0.0, 1.0)), __C.Vertex(color: SIMD4<Float>(0.0, 0.0, 1.0, 1.0), pos: SIMD2<Float>(1.0, -1.0))]
```


- 型確認

```
print(type(of: vertices))
```

```
Array<Vertex>
```



## 📝 2021/07/04

三角形ハロワ挑戦中



`vertex` 定義を`ctypes` で問題がないのか悩みつつ、色々なリファレンスを調査中


xcode 上で定義するもの(呼び出す？)もあり、まだ整理できていない



## 📝 2021/07/03

シェーダー描画用として関数分けて書いた方が良さそう

## 📝 2021/07/02

```
commandBuffer = commandQueue.commandBuffer()
AttributeError: 'NoneType' object has no attribute 'commandBuffer'

```


delegate のinitialize で、`commandQueue` を持たせる方法が見つからなかったので


view でdelegate をセットする前に


```
renderer = pyRenderer.alloc().init()
renderer.commandQueue = self.mtkView.device().newCommandQueue()
self.mtkView.setDelegate_(renderer)

```

として、delegate内のメソッドでも呼べるようにしてみた





ずっと、呼んでるかもで、いきなり落ちる時はある、、、


## 📝 2021/07/01

### delegate まわり

`drawInMTKView_` の呼び出し




```
renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
    renderPassDescriptor)

renderEncoder.endEncoding()
commandBuffer.presentDrawable_(view.currentDrawable())
commandBuffer.commit()
```

ここは、一括で処理しないと落ちた

`renderEncoder` 格納のみ書いてて、だめだと思って`commit()` までだーっと書いたら行けた


#### `commandBuffer`

初回呼び出しの数秒後(5秒くらい)と、2回目以降の呼び出し直後で以下エラー吐き出し

```
commandBuffer = commandQueue.commandBuffer()
AttributeError: 'NoneType' object has no attribute 'commandBuffer'

```


Python 側ではなくobjc-util 側だから取り回しがめんどう


## 📝 2021/06/30

`CAMetalLayer` がもやっとするので、`MTKView` かなぁと


[Metal 3D Graphics Part 1: Basic Rendering](https://donaldpinckney.com/metal/2018/07/05/metal-intro-1.html) これ参考にしてる

順番にフォルダ作ってやってみる


### 方針


いつもほぼ、一緒だけど


なるべく、`objc_util` を避けつつ実装

ui モジュールで行けるなら行ける的な


`View` classがクソでかになりそうだけども、ビジュアル系(?) って往々にしてそうなりがちな気がしてるから今の所そのまま


`setなんたら_(なにか)` で呼べるものは、`set` で呼ぶ



## 📝 2021/06/29

Protocol の `MTLDevice`

```
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
device = ObjCInstance(MTLCreateSystemDefaultDevice())

```

`MTLBuffer`

```
let dataSize = vertexData.count * MemoryLayout.size(ofValue: vertexData[0])
vertexBuffer = device.makeBuffer(bytes: vertexData, length: dataSize, options: [])
```
```
dataSize = len(vertexData) * 16
vertexBuffer = device.newBufferWithBytes_length_options_(ns(vertexData), dataSize, 0)
```
`float` だから16 やろ！という安直な考え


ループの処理の部分で無理しそうと感じてる




## 📝 2021/06/13


``` .py
from objc_util import *
from pprint import pprint

pprint(dir())

'''
['CGAffineTransform',
 'CGFloat',
 'CGPoint',
 'CGRect',
 'CGSize',
 'CGVector',
 'LP64',
 'NSArray',
 'NSBundle',
 'NSData',
 'NSDictionary',
 'NSEnumerator',
 'NSInteger',
 'NSMutableArray',
 'NSMutableData',
 'NSMutableDictionary',
 'NSMutableSet',
 'NSMutableString',
 'NSNotFound',
 'NSNumber',
 'NSObject',
 'NSRange',
 'NSSet',
 'NSString',
 'NSThread',
 'NSUInteger',
 'NSURL',
 'NSUTF8StringEncoding',
 'NS_UTF8',
 'ObjCBlock',
 'ObjCClass',
 'ObjCClassMethod',
 'ObjCInstance',
 'ObjCInstanceMethod',
 'POINTER',
 'Structure',
 'UIApplication',
 'UIBezierPath',
 'UIColor',
 'UIEdgeInsets',
 'UIImage',
 'UIView',
 '__annotations__',
 '__builtins__',
 '__cached__',
 '__doc__',
 '__file__',
 '__loader__',
 '__name__',
 '__package__',
 '__spec__',
 'byref',
 'c',
 'c_bool',
 'c_byte',
 'c_char',
 'c_char_p',
 'c_double',
 'c_float',
 'c_int',
 'c_int32',
 'c_long',
 'c_longlong',
 'c_short',
 'c_ubyte',
 'c_uint',
 'c_ulong',
 'c_ulonglong',
 'c_ushort',
 'c_void_p',
 'create_objc_class',
 'load_framework',
 'ns',
 'nsdata_to_bytes',
 'nsurl',
 'on_main_thread',
 'pointer',
 'pprint',
 'release_global',
 'retain_global',
 'sel',
 'sizeof',
 'uiimage_to_png']

'''

```


## 📝 2021/06/11


`objc-util` と`ctypes` を使う


```
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = c_void_p

```

`CAMetalLayer` ではなく、`MTKView` かなぁ

- `class`
- `InstanceMethod`
	- `()` で呼ぶ
- `function`
	- `c.` で呼び出す



- [Is it possible to use MetalKit with objc_util | forum.omz-software.com](https://forum.omz-software.com/topic/6646/is-it-possible-to-use-metalkit-with-objc_util)

- [Metal を使って10万個のパーティクルを描画しよう](https://qiita.com/naru-jpn/items/9f4f1624495f3e72d6f9)
	- [naru-jpn / 100000-particles](https://github.com/naru-jpn/100000-particles)
- [Metal Tutorial: Getting Started | raywenderlich.com](https://www.raywenderlich.com/7475-metal-tutorial-getting-started)

