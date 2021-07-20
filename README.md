# pystaMetalStudy

Pythonista でMetal やる

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

