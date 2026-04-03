/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useService } from "@web/core/utils/hooks";
import { debounce } from "@web/core/utils/timing";
import { Domain } from "@web/core/domain";
import { _t } from "@web/core/l10n/translation";

const origGetGroupNameCellColSpan = ListRenderer.prototype.getGroupNameCellColSpan;

patch(ListRenderer.prototype, {
    setup() {
        this.mlnService = useService("mln_advanced_list");
        this.mlnNotification = useService("notification");
        this.orm = useService("orm");
        super.setup();
        this._mlnDebouncedReload = debounce(() => this._mlnReloadListDomain(), 400);
    },

    /**
     * Main window lists: env.searchModel matches list model. Embedded x2many lists
     * use a different resModel and are excluded. Do not pass a custom Owl prop
     * (ListRenderer props are strict and static patch is unreliable in assets).
     */
    get mlnAdvEnabled() {
        const sm = this.env.searchModel;
        if (!sm) {
            return true;
        }
        return sm.resModel === this.props.list.resModel;
    },

    get nbCols() {
        let nbCols = this.columns.length;
        if (this.hasSelectors) {
            nbCols++;
        }
        if (this.hasActionsColumn) {
            nbCols++;
        }
        if (this.hasOpenFormViewColumn) {
            nbCols++;
        }
        if (this.mlnAdvEnabled) {
            nbCols++;
        }
        return nbCols;
    },

    getGroupNameCellColSpan(group) {
        let colspan = origGetGroupNameCellColSpan.call(this, group);
        if (this.mlnAdvEnabled) {
            colspan = Math.max(1, colspan - 1);
        }
        return colspan;
    },

    _mlnIsColumnSearchable(column) {
        if (!column || column.type !== "field") {
            return false;
        }
        if (column.widget === "handle" || column.widget === "properties") {
            return false;
        }
        const field = this.fields[column.name];
        if (!field) {
            return false;
        }
        return [
            "char",
            "text",
            "html",
            "many2one",
            "many2many",
            "selection",
            "integer",
            "float",
            "monetary",
            "boolean",
            "date",
            "datetime",
        ].includes(field.type);
    },

    /**
     * One quick-filter per visible list column (matches current tree fields).
     */
    getMlnFilterMetaForColumn(column) {
        if (!this.mlnAdvEnabled || !this._mlnIsColumnSearchable(column)) {
            return null;
        }
        const pref = this.mlnService.getPreference();
        const line = (pref?.filter_lines || []).find((l) => l.field_name === column.name);
        const label = column.label || column.name;
        const field = this.fields[column.name];
        let defaultPh = _t("Search by %s", label);
        if (field?.type === "date" || field?.type === "datetime") {
            defaultPh = _t("Date: 2024-01-15, 2024-03, 2024 or 15/01/2024");
        } else if (field?.type === "many2many") {
            defaultPh = _t("Search linked records by name");
        }
        const placeholder =
            line?.placeholder && String(line.placeholder).trim()
                ? line.placeholder
                : defaultPh;
        const filters = this.mlnService.getColumnFilters();
        return {
            field_name: column.name,
            placeholder,
            value: filters[column.name] ?? "",
        };
    },

    get mlnShowColumnFilterRow() {
        if (!this.mlnAdvEnabled) {
            return false;
        }
        return this.columns.some((c) => this._mlnIsColumnSearchable(c));
    },

    getMlnRowNumber(record, group) {
        if (!this.mlnAdvEnabled) {
            return "";
        }
        const list = group?.list || this.props.list;
        const idx = list.records.indexOf(record);
        if (idx < 0) {
            return "";
        }
        return list.offset + idx + 1;
    },

    onMlnFilterInput(fieldName, ev) {
        this.mlnService.setColumnFilter(fieldName, ev.target.value);
        this._mlnDebouncedReload();
    },

    async _mlnReloadListDomain() {
        const sm = this.env.searchModel;
        const model = this.props.list.model;
        if (!sm || !model) {
            return;
        }
        let domain = sm.domain;
        const extra = await this.mlnService.buildExtraDomainAsync(
            this.orm,
            this.props.list.resModel,
            this.fields
        );
        if (extra && extra.length) {
            domain = Domain.and([domain, extra]).toList();
        }
        await model.load({ domain });
        this.render(true);
    },

    async onMlnResetFilters() {
        this._mlnDebouncedReload?.cancel?.();
        this.mlnService.activateForList(this.props.list.resModel);
        await this._mlnReloadListDomain();
    },

    _mlnCollectExportData() {
        const cols = this.columns.filter((c) => c.type === "field");
        const headers = cols.map((c) => c.label || c.name);
        const rows = [];
        const walk = (lst) => {
            if (lst.isGrouped) {
                for (const g of lst.groups || []) {
                    if (!g.isFolded) {
                        walk(g.list);
                    }
                }
            } else {
                for (const record of lst.records || []) {
                    const line = [];
                    for (const col of cols) {
                        if (this.evalInvisible(col.invisible, record)) {
                            line.push("");
                            continue;
                        }
                        try {
                            const raw = this.getFormattedValue(col, record);
                            line.push(this._mlnStripHtml(String(raw ?? "")));
                        } catch {
                            line.push("");
                        }
                    }
                    rows.push(line);
                }
            }
        };
        walk(this.props.list);
        return { headers, rows };
    },

    _mlnStripHtml(html) {
        const d = document.createElement("div");
        d.innerHTML = html;
        return (d.textContent || "").replace(/\s+/g, " ").trim();
    },

    async onMlnExport(format) {
        const { headers, rows } = this._mlnCollectExportData();
        if (!rows.length) {
            this.mlnNotification.add(_t("No rows to export."), { type: "warning" });
            return;
        }
        try {
            const result = await this.mlnService.exportFile(
                this.orm,
                format,
                headers,
                rows,
                this.props.list.resModel
            );
            const bin = atob(result.data_b64);
            const bytes = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) {
                bytes[i] = bin.charCodeAt(i);
            }
            const blob = new Blob([bytes], { type: result.mimetype });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = result.filename;
            a.click();
            URL.revokeObjectURL(url);
        } catch (e) {
            this.mlnNotification.add(e.message || String(e), { type: "danger" });
        }
    },

    async onMlnCopy() {
        const { headers, rows } = this._mlnCollectExportData();
        const text = [headers.join("\t"), ...rows.map((r) => r.join("\t"))].join("\n");
        try {
            await navigator.clipboard.writeText(text);
            this.mlnNotification.add(_t("Copied to clipboard."), { type: "success" });
        } catch {
            this.mlnNotification.add(_t("Clipboard not available."), { type: "warning" });
        }
    },
});
