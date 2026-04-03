/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { Domain } from "@web/core/domain";

const originalLoad = RelationalModel.prototype.load;

patch(RelationalModel.prototype, {
    async load(params = {}) {
        const svc = this.env.services?.mln_advanced_list;
        if (
            svc &&
            params.resModel &&
            svc.isActiveRootList(params.resModel) &&
            !this.config.isMonoRecord
        ) {
            const fields = this.config.fields || {};
            const orm = this.env.services.orm;
            const extra = await svc.buildExtraDomainAsync(orm, params.resModel, fields);
            if (extra && extra.length) {
                const base = params.domain || [];
                params = { ...params, domain: Domain.and([base, extra]).toList() };
            }
        }
        return originalLoad.call(this, params);
    },
});
