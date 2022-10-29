模块使用说明
===============
扩展JsonRPC返回数据格式
custom=True 开启自定义数据格式

案例：

@http.route('/custom/api', type='json', methods=['POST'], auth='none', csrf=False, custom=True)
def custom_api(self, **kw):
    data = request.jsonrequest
        ...
        ...
        ...
    return {"code": 300, 'result': 'fail', "message": "系统中没有找到设备"}
