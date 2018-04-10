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

## 接口样例 -- 支持解析/过滤/ 和/**/注释（Pretty Json不支持)
```
[  // 第一个接口，最小配置，默认headers {Content-Type: application/wwwurlencode}
  {
    "url": "http://192.168.100.238:8089/api/Istation/matchStation",
    "data": {
      "lng": "116.123",
      "lat": "93.123"
    }
  },
  // 第二各接口，全参数示例
  {
    "method": "POST",   // GET, POST , PUT, HEAD, ...
    "uri": "/api/Istation/matchStation",    // base_url 从配置文件中读取
    "headers": {
      "Content-Type": "application/json; utf-8"
    },
    "cookies": {},    //支持Cookies
    "data": {
      "lng": "${data1[0]}",    //source字段data1对应的数据文件中的第1列，循环取
      "lat": "${data1[1]}"
    },
    "session": "login",     //是否调用需要登录

    
    "source": {             // 数据文件
      "data1": "data.txt",
      "data2": "data.txt"
    },
    "sign": "station",     // 签名字段


    "store_response": {    // 存储response中的字段，可用于同文件，该api之后的api使用
      "code": "response.code"
    },

    "concurrency": 1,     // 并发数
    "times": 2,           // 总执行次数

    "tags": ["sample", "no-run"],    // 标签，永远测试时有选择的执行

    "setup": {"DB-198":["UPDATE SET amount = 100 WHERE station_id=57 and goods_code='DP';", 
            "UPDATE SET amount = 100 WHERE station_id=57 and goods_code='MX';"]},  // 执行该接口前准备
    "teardown": {"DB-198":["UPDATE SET amount = 0 WHERE station_id=57 and goods_code='DP';", 
            "UPDATE SET amount = 0 WHERE station_id=57 and goods_code='MX';"]},   //执行该接口后清理

    "assert": "response.code == \"100000\""   // 断言response
  }
]```


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
* 不容易区分参数是否必选

"assert_response":"\"code\":100000"   # assert json.dumps(response)  contains "code":100000
"assert_response":{"code":100000, "error": 0}   # assert response["code"] == 100000 and response["error"] == 0  if response is not json,response = json.loads(response)
"assert_response": null ---default   assert response code=200


