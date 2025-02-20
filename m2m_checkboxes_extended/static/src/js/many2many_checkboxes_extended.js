import { registry } from "@web/core/registry";

const originalComponent = registry.category("fields").get("many2many_checkboxes");

export class Many2ManyCheckboxesFieldExtended extends originalComponent.component {
    static template = "zdt_elderly_abilities.Many2ManyCheckboxesFieldExtended";

    setup() {
        super.setup();
        // ✅ 确保 colCount 传递正确（默认为 1）
        this.colCount = this.props.options?.col_count || 1;
    }
}

export const many2ManyCheckboxesFieldExtended = {
    component: Many2ManyCheckboxesFieldExtended,
    displayName: "Checkboxes Extended",
    supportedTypes: ["many2many"],
    isEmpty: () => false,
    extractProps(fieldInfo, dynamicInfo) {
        return {
            ...originalComponent.extractProps(fieldInfo, dynamicInfo),
            options: fieldInfo.options || {},
        };
    },
};

// ** 注册新的字段组件 **
registry.category("fields").add("many2many_checkboxes_extended", many2ManyCheckboxesFieldExtended);
