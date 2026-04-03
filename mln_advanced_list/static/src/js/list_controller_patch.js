/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, onWillUnmount, useState, useSubEnv } from "@odoo/owl";

patch(ListController.prototype, {
    setup() {
        const mlnService = useService("mln_advanced_list");
        const orm = useService("orm");
        this.mlnListPref = useState({ loaded: false, inlineEdit: true });

        useSubEnv({
            mlnReloadPreference: async () => {
                try {
                    const data = await orm.call(
                        "mln.advanced.list.preference",
                        "mln_get_for_user_model",
                        [this.props.resModel]
                    );
                    this.mlnListPref.inlineEdit = data.inline_edit;
                    mlnService.setPreference(data);
                } catch {
                    mlnService.setPreference(null);
                }
            },
        });

        onWillStart(async () => {
            try {
                const data = await orm.call(
                    "mln.advanced.list.preference",
                    "mln_get_for_user_model",
                    [this.props.resModel]
                );
                this.mlnListPref.inlineEdit = data.inline_edit;
                mlnService.setPreference(data);
            } catch {
                mlnService.setPreference(null);
            } finally {
                this.mlnListPref.loaded = true;
            }
        });

        super.setup();
        this._mlnArchListEditable = this.editable;
        mlnService.activateForList(this.props.resModel);

        onWillUnmount(() => {
            mlnService.deactivateList();
        });
    },

    get mlnEffectiveEditable() {
        if (!this.mlnListPref.loaded) {
            return this._mlnArchListEditable;
        }
        if (!this.mlnListPref.inlineEdit) {
            return false;
        }
        return this._mlnArchListEditable;
    },
});
