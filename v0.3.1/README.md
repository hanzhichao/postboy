# PostBoy---基于json文件数据驱动的接口测试框架

## Fixture
* 接口数据基于json文件
* 支持集成sublime text
* 支持接口签名
* 支持login required
* 支持concurrency and times---并发和多轮
* 支持response assert
* 支持application/json 及 wwwurlencoded headers
* 支持携带cookies
* 支持type指定接口类型
* 支持senarios按序执行
* 支持批量测试目录下所有接口 含子目录

## 使用方法
1. clone或下载项目
2. 新建json，api文件,例如getUserById.json
3. 命令行运行 python post.py getUserByID.json

## 接口样例
1. 最少参数样例
```
{
  "uri": "http://****/api/user/getInfoById",
  "data": {"id": "51"}
}
```
2. 最多参数样例
```
[
  {
    "url": "http://192.168.100.238:8089/api/Istation/matchStation",
    "data": {
      "lng": "116.123",
      "lat": "93.123"
    }
  },
  {
    "method": "POST",
    "uri": "/api/Istation/matchStation",
    "headers": {
      "Content-Type": "application/json; utf-8"
    },
    "cookies": {},
    "data": {
      "lng": "${data1[0]}",
      "lat": "${data1[1]}"
    },
    "session": "login",
    "source": {
      "data1": "data.txt",
      "data2": "data.txt"
    },
    "sign": "station",
    "store_response": {
      "code": "response.code"
    },
    "concurrency": 1,
    "times": 2,
    "tags": [
      "sample",
      "no-run"
    ],
    "setup": {
      "DB-198": [
        "UPDATE SET amount = 100 WHERE station_id=57 and goods_code='DP';",
        "UPDATE SET amount = 100 WHERE station_id=57 and goods_code='MX';"
      ]
    },
    "teardown": {
      "DB-198": [
        "UPDATE SET amount = 0 WHERE station_id=57 and goods_code='DP';",
        "UPDATE SET amount = 0 WHERE station_id=57 and goods_code='MX';"
      ]
    },
    "assert": "response.code == \"100000\""
  }
]
```

## Sublime Text  编译json接口，使用方法
1. Sublime Text3 -> Tools -> Build System -> New Build System
2. 输入以下内容，保存为postboy.sublime-build 
```
{
    "cmd": ["python","D:/Projects/postboy/post.py","$file"],
    "file_regex": "^[ ] *File \"(...*?)\", line ([0-9]*)",
    "selector": "source.json",
}
```
3. 在json接口文件窗口，选择编译系统为postboy(或自动)，按Ctrl+B 编译

## 已知问题
* json数据文件不支持注释
* 不容易区分参数是否必选

"assert_response":"\"code\":100000"   # assert json.dumps(response)  contains "code":100000
"assert_response":{"code":100000, "error": 0}   # assert response["code"] == 100000 and response["error"] == 0  if response is not json,response = json.loads(response)
"assert_response": null ---default   assert response code=200
