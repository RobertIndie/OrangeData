# Orange Data

这是我在和同学Azusa闲聊的过程中构思的一个程序。

## 场景

买一包香橙，扫一下上面的二维码，立刻得知这袋橙子从种子来源地到橙子采摘装袋时间一系列数据。

厂商给这个商品一个标识，并且这个标识是他人无法篡改的，验证方可以读取这个标识，得到各种数据，并且这些数据是可信的。

## 原理

详见orangedata.py

Process:

![process](.\assets\process.png)

Validate:

![validate](.\assets\validate.png)

Block data example:

```json
{
	"prevBlock": "0a1b2ac1dc9d00f4bff6f290c4ac3434175925eb95671fe461a44c19658101381ef0dfefd2b75fd2c0e4f048a0d180514048f564b618257cb6df1c0b3ba6bb224e6838bf12fd827f6e4251514c0577a7e53cbe022052f47c574f7366dcf696708441d49fca817e1d26f8dd58b069ce424fff417918f86f00e3812ea9803c8df838ada2ac95d15f663c438a6648c7f86c9f65f869c358de0da829a527a5f87d2dbdcd73d091c764a8daa2f707cdfdc44a4cdc99f9200fbee5f65e1b27f36ef4df7b30c0f21ee196277e1444697e40d8f6e381c8b36f9cced5b765134f2222c177daa2e39cee389be54ec76516ad2ad5615082ee894c9fabb4c42e42af3bdd7fd6",
	"processName": "食品加工",
	"factoryName": "食品加工厂",
	"data": "第366天，购买香橙；第368天，加工香橙，更香了；第369天，出售。"
}
```

