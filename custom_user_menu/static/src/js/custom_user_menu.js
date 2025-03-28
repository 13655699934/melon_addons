/** @odoo-module **/

import { registry } from "@web/core/registry";

// 定义要移除的菜单项
const itemsToRemove = [
    "documentation",
    "support",
    "shortcuts",
    "profile",
    "odoo_account",
    "install_pwa",
    "settings",
    "separator"
];

// 安全地移除指定的菜单项
itemsToRemove.forEach(item => {
    registry.category("user_menuitems").remove(item);
});
