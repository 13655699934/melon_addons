                 
========================安装说明=============================
-------------------------------------------------------------
** 安装说明：本模块依赖 web ** 
欢迎技术交流：微信号: melon20200809 项目开发请联系：13655699934


=====================模块功能点================================
-------------------------------------------------------------
**    模块功能点：实现禁止选用小于当前的日期时间    **
-------------------------------------------------------------
实现功能：
  1、实现禁止选用小于当前的日期时间


-------------------------------------------------------------



=====================模块使用说明================================
--------------------------------------------------------------
在类型是Date或Datetime类型的字段上添加挂件：

一、安装此挂件模块：

二、
    在py里面定义好字段：
    order_date=fields.Date(u'单据日期')
    order_date2=fields.Datetime(u'订单时间')

   在xml里面写widget="disable_date_widget"即可：
   <field name="order_date" widget="disable_date_widget"/>
   <field name="order_datetime" widget="disable_datetime_widget"/>


--------------------------------------------------------------