import web
from wsgiref.simple_server import make_server
import json
import SimTyphoonForm
import SimTyphoonLand

urls = ('/SimTyphoon', 'SimTyphoon')

app = web.application(urls, globals())


class SimTyphoon:

    def POST(self):
        try:
            input_data = web.data()  # 获取原始请求数据
            json_data = json.loads(input_data)
            value1 = json_data.get('typhoonName')
            value2 = json_data.get('typhoonTime')
            value3 = json_data.get('method')

            if value1 is None or value2 is None:
                raise ValueError("Both value1 and value2 must be provided.")
            if value3 == "Form":
                res = SimTyphoonForm.typhoonForm(value1)
                results = res[0]
            elif value3 == "Land":
                res = SimTyphoonLand.typhoonLand(value1)
                results = res[0]

            response_data = {'result': results}
            response_json = json.dumps(response_data)

            web.header('Content-Type', 'application/json')
            return response_json
        except Exception as e:
            error_message = {'error': f"An error occurred: {str(e)}"}
            web.header('Content-Type', 'application/json')
            return json.dumps(error_message)


if __name__ == "__main__":
    httpd = make_server('', 8070, app.wsgifunc())
    httpd.serve_forever()
    app.run()
