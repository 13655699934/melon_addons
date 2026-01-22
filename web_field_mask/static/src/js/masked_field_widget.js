/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

export class MaskedFieldWidget extends Component {
    static template = "web_field_mask.MaskedFieldWidget";

    static props = {
        ...standardFieldProps,
        mask_type: { type: String, optional: true },
        mask_start: { type: Number, optional: true },
        mask_end: { type: Number, optional: true },
        mask_char: { type: String, optional: true },
        show_on_hover: { type: Boolean, optional: true },

        // 可选：是否默认允许点击进入编辑（默认 true）
        allow_edit: { type: Boolean, optional: true },
    };

    static defaultProps = {
        mask_type: "id_card",
        mask_char: "*",
        show_on_hover: true,
        allow_edit: true,
    };

    setup() {
        this.notification = useService("notification");
        this.state = useState({
            showOriginal: false, // hover 显示原文
            editing: false,      // 是否处于输入框编辑态
        });
    }

    get originalValue() {
        const v = this.props.record?.data?.[this.props.name];
        return v == null ? "" : String(v);
    }

    get canEdit() {
        // Odoo 允许编辑：页面不是 readonly + 组件不是 readonly + allow_edit
        return !this.props.readonly && (this.props.allow_edit !== false);
    }

    get displayValue() {
        // 默认脱敏；如果 hover 显示原文则显示原文
        if (this.state.showOriginal) return this.originalValue;
        return this.maskedValue;
    }

    get maskedValue() {
        const value = this.originalValue;
        if (!value) return "";

        const maskType = this.props.mask_type || "phone";
        const maskChar = this.props.mask_char || "*";

        switch (maskType) {
            case "phone":
                return this.maskPhone(value, maskChar);
            case "id_card":
                return this.maskIdCard(value, maskChar);
            case "bank_card":
                return this.maskBankCard(value, maskChar);
            case "email":
                return this.maskEmail(value, maskChar);
            case "name":
                return this.maskName(value, maskChar);
            case "custom":
                return this.maskCustom(
                    value,
                    this.props.mask_start ?? 3,
                    this.props.mask_end ?? 4,
                    maskChar
                );
            default:
                return this.maskPhone(value, maskChar);
        }
    }

    maskPhone(value, maskChar) {
        if (value.length < 11) return value;
        return value.substring(0, 3) + maskChar.repeat(4) + value.substring(7);
    }

    maskIdCard(value, maskChar) {
        if (value.length < 15) return value;
        return value.substring(0, 3) + maskChar.repeat(value.length - 7) + value.substring(value.length - 4);
    }

    maskBankCard(value, maskChar) {
        const cleaned = value.replace(/\s/g, "");
        if (cleaned.length < 12) return value;
        const first4 = cleaned.substring(0, 4);
        const last4 = cleaned.substring(cleaned.length - 4);
        const middle = maskChar.repeat(4);
        return `${first4} ${middle} ${middle} ${last4}`;
    }

    maskEmail(value, maskChar) {
        if (!value.includes("@")) return value;
        const [username, domain] = value.split("@");
        if ((username || "").length <= 3) return value;
        return username.substring(0, 3) + maskChar.repeat(3) + "@" + domain;
    }

    maskName(value, maskChar) {
        if (value.length < 2) return value;
        return value.charAt(0) + maskChar.repeat(value.length - 1);
    }

    get compactMode() {
        return ["list", "tree", "kanban"].includes(this.props.viewType);
    }

    maskCustom(value, start, end, maskChar) {
        if (value.length <= start + end) return value;
        const prefix = value.substring(0, start);
        const suffix = value.substring(value.length - end);
        const middle = maskChar.repeat(value.length - start - end);
        return prefix + middle + suffix;
    }

    onMouseEnter() {
        if (this.props.show_on_hover && !this.state.editing) {
            this.state.showOriginal = true;
        }
    }

    onMouseLeave() {
        this.state.showOriginal = false;
    }

    startEdit() {
        if (!this.canEdit) return;
        this.state.editing = true;
        this.state.showOriginal = true; // 进入编辑时显示原文
    }

    stopEdit() {
        this.state.editing = false;
        this.state.showOriginal = false;
    }

    onInput(ev) {
        this.props.record.update({ [this.props.name]: ev.target.value });
    }

    onKeydown(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this.stopEdit();
        }
        if (ev.key === "Escape") {
            ev.preventDefault();
            this.stopEdit();
        }
    }

    onCopyOriginal() {
        const v = this.originalValue;
        if (!v) return;
        navigator.clipboard?.writeText(v);
        this.notification.add("已复制完整内容", { type: "success" });
    }
}


registry.category("fields").add("masked_field", {
    component: MaskedFieldWidget,
    supportedTypes: ["char", "text"],
    extractProps: ({ attrs, options, viewType }) => ({
        viewType, // ✅ 新增：form/list/kanban…
        mask_type: (options && options.mask_type) || attrs.mask_type,
        mask_start:
            (options && options.mask_start) ??
            (attrs.mask_start ? Number(attrs.mask_start) : undefined),
        mask_end:
            (options && options.mask_end) ??
            (attrs.mask_end ? Number(attrs.mask_end) : undefined),
        mask_char: (options && options.mask_char) || attrs.mask_char,
        allow_edit:
            (options && options.allow_edit) ??
            (attrs.allow_edit === undefined
                ? true
                : ["1", "true", "True"].includes(String(attrs.allow_edit))),
        show_on_hover:
            (options && options.show_on_hover) ??
            (attrs.show_on_hover === undefined
                ? true
                : ["1", "true", "True"].includes(String(attrs.show_on_hover))),
    }),
});

