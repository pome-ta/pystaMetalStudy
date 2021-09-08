# pystaMetalStudy

[Pythonista 3](http://omz-software.com/pythonista/) でMetal をチャレンジするリポリトリ

さまざまなサイトを参照しているので、参照URL などは、各ディレクトリ内に明記予定


以下列記は、実装日誌的なメモ


## 📝 2021/09/08


`animateBy` の数値をとらないけないから

06 に戻り、時間を取得してみる



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
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.9977786, 0.0, 0.066617295, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.066617295, 0.0, 0.9977786, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9978  0.0000  0.0666  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0666  0.0000  0.9978  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9977786, 0.0, 0.066617295, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.066617295, 0.0, 0.9977786, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.99652976, 0.0, 0.08323692, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.08323692, 0.0, 0.99652976, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9965  0.0000  0.0832  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0832  0.0000  0.9965  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.99652976, 0.0, 0.08323692, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.08323692, 0.0, 0.99652976, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.9950042, 0.0, 0.09983342, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.09983342, 0.0, 0.9950042, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9950  0.0000  0.0998  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.0998  0.0000  0.9950  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9950042, 0.0, 0.09983342, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.09983342, 0.0, 0.9950042, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.99320215, 0.0, 0.11640219, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.11640219, 0.0, 0.99320215, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9932  0.0000  0.1164  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.1164  0.0000  0.9932  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.99320215, 0.0, 0.11640219, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.11640219, 0.0, 0.99320215, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.9911243, 0.0, 0.13293862, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.13293862, 0.0, 0.9911243, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9911  0.0000  0.1329  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.1329  0.0000  0.9911  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9911243, 0.0, 0.13293862, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.13293862, 0.0, 0.9911243, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.9887711, 0.0, 0.14943814, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.14943814, 0.0, 0.9887711, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9888  0.0000  0.1494  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.1494  0.0000  0.9888  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.9887711, 0.0, 0.14943814, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.14943814, 0.0, 0.9887711, 0.0], [0.0, 0.0, 0.0, 1.0]])
▿ simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
  -  : " 1.0000  0.0000  0.0000  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : " 0.0000  0.0000  1.0000  0.0000"
  -  : " 0.0000  1.5000  0.0000  1.0000"
simd_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.5, 0.0, 1.0]])
▿ simd_float4x4([[0.98614323, 0.0, 0.16589613, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.16589613, 0.0, 0.98614323, 0.0], [0.0, 0.0, 0.0, 1.0]])
  -  : " 0.9861  0.0000  0.1659  0.0000"
  -  : " 0.0000  1.0000  0.0000  0.0000"
  -  : "-0.1659  0.0000  0.9861  0.0000"
  -  : " 0.0000  0.0000  0.0000  1.0000"
simd_float4x4([[0.98614323, 0.0, 0.16589613, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.16589613, 0.0, 0.98614323, 0.0], [0.0, 0.0, 0.0, 1.0]])
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

