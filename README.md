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
```
{
  "url": "http://192.168.100.238:8082/api/user/getInfoById",
  "sign": {
    "accessId": "CORE0001",
    "accessKey": "BMLYkAKNcAthZbW7kQDUe8i4PmLoek"
  },
  "data": {
    "id": "51"
  },
  "remark":"根据用户ID获取用户信息"
}
```
需要替换参数的接口样例---指定fromat_data : true
```
{
  "uri": "/api/ITakeaway/w",
  "headers": {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  "cookies": {
    "PHPSESSID": "fd34e161b19433fb1cb39150cb5f17dc"
  },
  "concurrency": "5",
  "times": "10",
  "format_data": true,
  "data": {
    "params": "%s"
  },
  "_params": {
    "address_id": "64948",
    "delivery_date": "2018-01-18",
    "start_time": "10:42:25",
    "end_time": "11:42:25",
    "is_reserve": "2",
    "invoice_id": "0",
    "money": "22.00",
    "discount": "0",
    "freight": "20.00",
    "received": "42.00",
    "is_invoice": "2",
    "is_activity": "2",
    "activity": "nothing",
    "red_envelope": "nothing",
    "pay_way": "2",
    "pay_channel": "4",
    "products": [
      {
        "id": "23",
        "num": "1"
      }
    ],
    "remark": "",
    "user_scope": "1",
    "channel": "14",
    "card_amount": "0",
    "card_id": "",
    "user_id": "83",
    "station_id": "53"
  },
}
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

