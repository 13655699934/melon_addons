                 
========================安装说明=============================
-------------------------------------------------------------
** 安装说明：本模块无依赖，直接应用界面安装即可 ** 
欢迎技术交流：微信号: melon20200809


=====================模块功能点================================
-------------------------------------------------------------
**    按钮实现搜索功能：可字段中指定路由、模型、条件     **
/**
<widget name="melon_btn_search" options='{
"url":"http://127.0.0.1:8099/api/v1/page/0","search":"name",
"model":"res.partner","fields":"name,email,mobile",
"domain":[["id",">", 0]],
"binding_fields":"name,email,mobile",
"pages":{"offset":0,"limit":10,"order":"id desc"}}'/>
**/
-------------------------------------------------------------


            
             
   

-------------------------------------------------------------