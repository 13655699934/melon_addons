/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Domain } from "@web/core/domain";

/**
 * @param {string} yStr
 * @param {string} moStr
 * @param {string} dStr
 */
function nextCalendarDayIso(yStr, moStr, dStr) {
    const y = Number(yStr);
    const mo = Number(moStr);
    const d = Number(dStr);
    const dt = new Date(y, mo - 1, d + 1);
    const yy = dt.getFullYear();
    const mm = String(dt.getMonth() + 1).padStart(2, "0");
    const dd = String(dt.getDate()).padStart(2, "0");
    return `${yy}-${mm}-${dd}`;
}

/**
 * Domain leaves for date/datetime column filter (ISO or DD/MM/YYYY).
 * @param {string} fname
 * @param {string} value
 * @param {"date" | "datetime"} fieldType
 * @returns {Array<[string, string, any]> | null}
 */
export function mlnParseDateFilterDomain(fname, value, fieldType) {
    const v = value.trim();
    if (!v) {
        return null;
    }

    let y;
    let mo;
    let d;
    const slashFull = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(v);
    if (slashFull) {
        d = Number(slashFull[1]);
        mo = Number(slashFull[2]);
        y = Number(slashFull[3]);
        if (mo < 1 || mo > 12 || d < 1 || d > 31) {
            return null;
        }
        const iso = `${y}-${String(mo).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
        return mlnParseDateFilterDomain(fname, iso, fieldType);
    }

    const isoFull = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v);
    if (isoFull) {
        const [, ys, mos, ds] = isoFull;
        const iso = `${ys}-${mos}-${ds}`;
        if (fieldType === "date") {
            return [
                [fname, ">=", iso],
                [fname, "<=", iso],
            ];
        }
        const next = nextCalendarDayIso(ys, mos, ds);
        return [
            [fname, ">=", `${iso} 00:00:00`],
            [fname, "<", `${next} 00:00:00`],
        ];
    }

    const isoMonth = /^(\d{4})-(\d{2})$/.exec(v);
    if (isoMonth) {
        const ys = isoMonth[1];
        const mos = isoMonth[2];
        y = Number(ys);
        mo = Number(mos);
        if (mo < 1 || mo > 12) {
            return null;
        }
        const start = `${ys}-${mos}-01`;
        const lastDay = new Date(y, mo, 0).getDate();
        const end = `${ys}-${mos}-${String(lastDay).padStart(2, "0")}`;
        if (fieldType === "date") {
            return [
                [fname, ">=", start],
                [fname, "<=", end],
            ];
        }
        const nextMonthStart =
            mo === 12
                ? `${y + 1}-01-01`
                : `${y}-${String(mo + 1).padStart(2, "0")}-01`;
        return [
            [fname, ">=", `${start} 00:00:00`],
            [fname, "<", `${nextMonthStart} 00:00:00`],
        ];
    }

    const isoYear = /^(\d{4})$/.exec(v);
    if (isoYear) {
        const ys = isoYear[1];
        const yn = Number(ys);
        if (fieldType === "date") {
            return [
                [fname, ">=", `${ys}-01-01`],
                [fname, "<=", `${ys}-12-31`],
            ];
        }
        return [
            [fname, ">=", `${ys}-01-01 00:00:00`],
            [fname, "<", `${yn + 1}-01-01 00:00:00`],
        ];
    }

    return null;
}

export const mlnAdvancedListService = {
    dependencies: ["orm"],

    start(env, { orm }) {
        const state = {
            activeResModel: null,
            /** @type {Record<string, string>} */
            columnFilters: {},
            /** @type {{ filter_lines: any[], inline_edit: boolean } | null} */
            preference: null,
        };

        return {
            activateForList(resModel) {
                state.activeResModel = resModel;
                state.columnFilters = {};
            },
            deactivateList() {
                state.activeResModel = null;
                state.columnFilters = {};
            },
            isActiveRootList(resModel) {
                return state.activeResModel === resModel;
            },
            setPreference(pref) {
                state.preference = pref;
            },
            getPreference() {
                return state.preference;
            },
            setColumnFilter(fieldName, value) {
                state.columnFilters[fieldName] = value;
            },
            getColumnFilters() {
                return state.columnFilters;
            },
            /**
             * Build extra AND domain from column filters (async for many2many name_search).
             * @param {import("@web/core/orm_service").ORM} ormService
             * @param {string} resModel
             * @param {Record<string, any>} fields
             */
            async buildExtraDomainAsync(ormService, resModel, fields) {
                const leaves = [];
                for (const [fname, raw] of Object.entries(state.columnFilters)) {
                    const v = (raw || "").trim();
                    if (!v || !fields[fname]) {
                        continue;
                    }
                    const type = fields[fname].type;
                    const fieldDef = fields[fname];

                    if (type === "many2many") {
                        const comodel = fieldDef.relation;
                        if (!comodel) {
                            continue;
                        }
                        try {
                            const tuples = await ormService.call(comodel, "name_search", [], {
                                name: v,
                                args: [],
                                operator: "ilike",
                                limit: 200,
                            });
                            const ids = (tuples || []).map((t) => t[0]);
                            if (ids.length) {
                                leaves.push([fname, "in", ids]);
                            } else {
                                leaves.push(["id", "in", []]);
                            }
                        } catch {
                            leaves.push(["id", "in", []]);
                        }
                        continue;
                    }

                    if (type === "date" || type === "datetime") {
                        const dleaves = mlnParseDateFilterDomain(fname, v, type);
                        if (dleaves) {
                            leaves.push(...dleaves);
                        }
                        continue;
                    }

                    if (type === "integer" || type === "float" || type === "monetary") {
                        const num = Number(v);
                        if (!Number.isNaN(num)) {
                            leaves.push([fname, "=", num]);
                        }
                    } else if (type === "boolean") {
                        const low = v.toLowerCase();
                        if (["1", "true", "yes", "y"].includes(low)) {
                            leaves.push([fname, "=", true]);
                        } else if (["0", "false", "no", "n"].includes(low)) {
                            leaves.push([fname, "=", false]);
                        }
                    } else {
                        leaves.push([fname, "ilike", v]);
                    }
                }
                if (!leaves.length) {
                    return [];
                }
                return Domain.and(leaves.map((l) => [l])).toList();
            },
            async exportFile(ormService, format, headers, rows, resModel) {
                return ormService.call("mln.advanced.list.preference", "mln_export_file", [
                    format,
                    headers,
                    rows,
                    resModel || false,
                ]);
            },
        };
    },
};

registry.category("services").add("mln_advanced_list", mlnAdvancedListService);
