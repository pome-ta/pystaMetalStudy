# pystaMetalStudy

Pythonista でMetal やる



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


`objc-util` と`ctypes` を使っていく


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
- []
