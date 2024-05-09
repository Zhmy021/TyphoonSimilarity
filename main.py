import web
import json
from wsgiref.simple_server import make_server
import os
import SimTyphoonForm
import SimTyphoonLand

urls = ('/TyphoonForm', 'TyphoonForm',
        '/TyphoonLand', 'TyphoonLand')

app = web.application(urls, globals())


class TyphoonForm:

    def POST(self):
        try:
            input_data = web.data()  # 获取原始请求数据
            print(input_data)
            json_data = json.loads(input_data)
            value1 = json_data.get('value1')
            value2 = json_data.get('value2')
            print(value1)
            if value1 is None or value2 is None:
                raise ValueError("Both value1 and value2 must be provided.")

            result_list = [value1, value2]
            result = ', '.join(result_list)

            response_data = {'result': result}
            response_json = json.dumps(response_data)

            web.header('Content-Type', 'application/json')
            return response_json
        except Exception as e:
            error_message = {'error': f"An error occurred: {str(e)}"}
            web.header('Content-Type', 'application/json')
            return json.dumps(error_message)


if __name__ == '__main__':
    # 设置端口号
    httpd = make_server('', 8070, app.wsgifunc())
    httpd.serve_forever()
    app.run()