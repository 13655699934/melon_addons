/** @odoo-module */
// 引入必要的模块
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

// 定义你的组件，继承自 Component
class IframeAction extends Component {
    static template = "templates_deepseek_ai_tag";
    // 你可以在这里添加组件的逻辑
}
// 在 actions 这个 category 下注册你的组件
registry.category("actions").add("deepseek_ai_tag", IframeAction);