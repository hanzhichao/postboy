import json
import optparse
import os
import requests
from jinja2 import Template


cli_opt = optparse.OptionParser()
cli_opt.add_option("--collect-only", action="store_true", dest="collect_only", help="列出所有用例")
cli_opt.add_option("--verbose", action="store", dest="verbose", help="显示级别: 1. 只显示用例结果 2. 只显示响应文本(默认) 3. 显示请求,响应及断言信息")
(options, args) = cli_opt.parse_args()


def postJson(path, timeout=60):
    try:
        with open(path, encoding='utf-8') as f:
            apis = json.load(f)

        if isinstance(apis, dict):
            apis=[apis]

        session = requests.session()
        for api in apis:

            # 处理全局变量
            str_api = json.dumps(api)
            if '%' in str_api:
                api = json.loads(str_api % globals())

            # 获取接口相关项
            url = api.get('url')
            method = api.get('method')
            headers = api.get('headers')
            cookies = api.get('cookies')
            params = api.get('params')
            data = api.get('data')
            files = api.get('files')
            _store = api.get('store')
            _assert = api.get('assert') # 系统变量 Response  Store  Assert Request Py  Sh Cmd  exec db Java JS

            # 如果json请求，转换一下数据
            if headers and 'json' in json.dumps(headers):
                data = json.dumps(data)

            # 根据method发送不同请求
            if method and method.lower() == 'get':
                response = session.get(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)
            else:
                response = session.post(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)

            # 存储中间结果
            if _store:
                for key in _store:
                    globals()[key]=eval(_store[key])
            
            # 处理响应
            try:
                response_text = json.dumps(response.json(), ensure_ascii=False, indent=2)
            except json.decoder.JSONDecodeError:  # only python3
                try:
                    response_text = response.text
                except UnicodeEncodeError:
                    # print(response.content.decode("utf-8","ignore").replace('\xa9', ''))
                    response_text = response.content
            finally:
                pass

            # 处理断言
            status = "PASS"
            if _assert:
                assert_results = []
                for item in _assert:
                    try:
                        assert eval(item)
                        assert_results.append("PASS: <%s>" % item)
                    except AssertionError:
                        assert_results.append("FAIL: <%s>" % item)
                        status = "FAIL"
                    except Exception as e:
                        assert_results.append("ERROR: <%s>\n%s" % (item, repr(e)))
                        status = "ERROR"  # 应放在post方法上
            
            # 打印结果
            if not options.verbose or options.verbose == '2':
                print(response_text)
            elif options.verbose == '3':
                print("="*80)
                print("请求:")
                print("Url: %s\nHeaders: %s\nData: %s" % (url, headers, data if isinstance(data, str) else json.dumps(data)))
                print("-"*80)
                print("响应:")
                print(response_text)
                if _assert:
                    print("-"*80)
                    print("断言:")
                    for assert_result in assert_results:
                        print(assert_result)
            else:
                print("%s --- %s" % (path, status))

    
    except IOError as e:
        print(e)

    except json.decoder.JSONDecodeError:
        print("json文件格式有误")


def discover(path="."):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith("test") and file.endswith(".json"):
                postJson(os.path.join(root, file))


def report():
    with open("report.tpl", encoding="utf-8") as f:
        report_body = f.read()
    t = Template(report_body)
    cases = [{"case_name": "case1", "result": "PASS"}, {"case_name": "case2", "result": "ERROR"}, {"case_name": "case3", "result": "PASS"}, {"case_name": "case4", "result": "FAIL"}]

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(t.render(title="PostJson测试报告", cases=cases))


def collect_only(path="."):
    count = 0
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                print(os.path.join(root, file))
                count += 1
        print("-"*80)
        print("Total: %d" % count)
               
def main():
    path = args[0] if args else "."
    if options.collect_only:
        collect_only() if not args else collect_only(args[0])
    else:
        postJson(path)


main()
# report()
