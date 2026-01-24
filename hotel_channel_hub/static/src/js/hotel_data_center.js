/** @odoo-module */
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class Center_Data_Hotel extends Component {
    static template = "templates_center_hotel_tag";
}


// 在 Odoo 18 的 `registry.category("actions")` 下注册组件
registry.category("actions").add("center_data_hotel_tags", Center_Data_Hotel);

