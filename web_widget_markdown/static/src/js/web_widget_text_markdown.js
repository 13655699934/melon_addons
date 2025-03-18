/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, markup, xml, useState } from "@odoo/owl";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { Mutex } from "@web/core/utils/concurrency";

/**
 * Markdown 文本字段小部件
 * 支持在表单视图中编辑和显示 Markdown 格式文本
 */
export class MarkdownField extends Component {
    static template = xml`
        <div class="o_field_markdown" t-att-class="{'o_field_readonly': props.readonly}">
            <div class="d-flex justify-content-end mb-2" t-if="!props.readonly">
                <button class="btn btn-sm btn-secondary toggle-preview-btn" t-on-click="togglePreview">
                    <t t-esc="state.isPreview ? '编辑' : '预览'"/>
                </button>
            </div>
            <div t-if="state.isPreview || props.readonly" class="markdown-preview border p-2 rounded">
                <div class="markdown-content" t-out="state.htmlContent"/>
            </div>
            <textarea t-else=""
                class="o_field_text_markdown_editor o_input" 
                t-ref="input"
                t-att-name="props.name"
                t-on-input="onInput"
                t-on-blur="onBlur"
                rows="10"
                t-model="state.value"/>
        </div>
    `;

    static props = {
        ...standardFieldProps,
        placeholder: { type: String, optional: true },
    };

    setup() {
        this.mutex = new Mutex();
        this.isDirty = false;

        this.state = useState({
            isPreview: false,
            value: this.props.record.data[this.props.name] || "",
            htmlContent: markup(this.convertToHtml(this.props.record.data[this.props.name] || "")),
        });

        useRecordObserver((record) => {
            if (!this.isDirty) {
                const newValue = record.data[this.props.name] || "";
                if (this.lastValue !== newValue) {
                    this.state.value = newValue;
                    this.state.htmlContent = markup(this.convertToHtml(newValue));
                    this.lastValue = newValue;
                }
            }
        });

        // 监听模型的保存事件
        const { model } = this.props.record;
        this.env.bus.addEventListener("WILL_SAVE_URGENTLY", () => this.commitChanges({ urgent: true }));
        model.bus.addEventListener("NEED_LOCAL_CHANGES", ({ detail }) => {
            detail.proms.push(this.commitChanges());
        });
    }
    
    /**
     * 切换预览模式
     */
    togglePreview() {
        if (this.props.readonly) {
            return;
        }
        this.state.isPreview = !this.state.isPreview;
        if (this.state.isPreview) {
            this.state.htmlContent = markup(this.convertToHtml(this.state.value));
        }
    }

    /**
     * 处理输入事件
     */
    onInput(ev) {
        if (this.props.readonly) {
            return;
        }
        this.state.value = ev.target.value;
        this.isDirty = true;
        this.props.record.model.bus.trigger("FIELD_IS_DIRTY", true);
    }

    /**
     * 处理失焦事件
     */
    async onBlur() {
        return this.commitChanges();
    }

    /**
     * 提交更改
     */
    async commitChanges({ urgent } = {}) {
        if (urgent) {
            this._commitChanges({ urgent });
        } else {
            return this.mutex.exec(() => this._commitChanges({ urgent }));
        }
    }

    /**
     * 内部提交更改方法
     */
    async _commitChanges({ urgent }) {
        if (this.isDirty) {
            this.lastValue = this.state.value;
            this.isDirty = false;
            await this.props.record.update({ [this.props.name]: this.state.value }).catch(() => {
                this.isDirty = true;
            });
            this.props.record.model.bus.trigger("FIELD_IS_DIRTY", this.isDirty);
        }
    }
    
    /**
     * 将 Markdown 转换为 HTML
     * @param {string} text 
     * @returns {string} HTML
     */
    convertToHtml(text) {
        if (!text) return "";
        
        // 简单的 Markdown 转换规则
        const html = text
            // 标题
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            // 斜体和粗体
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // 链接
            .replace(/\[([^\[]+)\]\(([^\)]+)\)/g, '<a href="$2">$1</a>')
            // 列表
            .replace(/^\s*\n\*/gm, '<ul>\n*')
            .replace(/^(\*.+)\s*\n([^\*])/gm, '$1\n</ul>\n\n$2')
            .replace(/^\*(.+)/gm, '<li>$1</li>')
            // 代码块
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            // 内联代码
            .replace(/`(.*?)`/g, '<code>$1</code>')
            // 引用
            .replace(/^\> (.*$)/gm, '<blockquote>$1</blockquote>');
            
        return html;
    }
}

// 注册字段组件
export const markdownField = {
    component: MarkdownField,
    displayName: _t("Markdown"),
    supportedTypes: ["text", "html"],
    extractProps({ attrs }) {
        return {
            placeholder: attrs.placeholder,
        };
    },
};

registry.category("fields").add("bootstrap_markdown", markdownField);
