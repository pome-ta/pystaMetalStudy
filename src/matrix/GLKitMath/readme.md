# matrix -> GLKitMath

## 参照先

メインの参照

- [Moving from OpenGL to Metal | raywenderlich.com](https://www.raywenderlich.com/9211-moving-from-opengl-to-metal)


Matrix 実装

- [OpenGLES-Pythonista / Cethric](https://github.com/Cethric/OpenGLES-Pythonista)
  - Pythonista でOpenGLES 走らせる的なプロジェクト
  - [OpenGLES-Pythonista/GLKit/glkmath/](https://github.com/Cethric/OpenGLES-Pythonista/tree/master/GLKit/glkmath)
    - その中の、`GLKit` で使われてる演算用関数をラップしているやつ



時間の取り回し

- [ここ](https://github.com/math-miki/MetalAdventCalendar/blob/master/MetalDay1/MetalDay1/Renderer.swift) の実装をお借りしてupdate毎 に加算するかたち
- `uniformBuffer` の`addCompletedHandler` が面倒に感じたので


