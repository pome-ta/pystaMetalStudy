# 📝 2023/11/04

## ポインタ整理


GPU がアクセスできるメモリにbuffer として保存しておく


```.py
buffer = device.newBufferWithLength(16, options=0)

print(f'Buffer is {buffer.length()} bytes in length')
#Buffer is 16 bytes in length
```

buffer のメモリサイズを16 bytes とする。中身は空の状態。


```.py
contents = buffer.contents()
```


buffer のメモリのポインタを取得。`UnsafeMutableRawPointer` を返す。

受け取っても、メモリの種類やサイズはわからない。


使いたい型情報にバインディングする。型付きポインタとして返す。





# 📝 2023/11/02

[Thirty Days of Metal — Day 2: Buffers | by Warren Moore | Medium](https://medium.com/@warrenm/thirty-days-of-metal-day-2-buffers-ec8c81040e3e)


