模块使用说明
===============
版本：18.0社区版
Version: 18.0 Community Edition

扩展JsonRPC返回数据格式
Extend JSON RPC return data format

功能说明：通过配置路由参数实现数据格式自定义
Function description: Customize data format by configuring routing parameters

使用说明：配置路由ext参数实现是否启动自定义数据格式功能_
Instructions for use: Configure the routing ext parameter to enable the custom data format function  

ext=True 开启自定义数据格式：仅针对 type='json'的路由接口
ext=True Enable custom data format: only for routing interfaces with type='json '

使用方法：
 @http.route('/api', type='json', methods=['POST'], auth='none', csrf=False, ext=True)


联系方式
==========================================
作者：hsx
微信号：H13655699934