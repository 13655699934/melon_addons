odoo.define('odoo_form_condition', function (require) {
    "use strict";
    var FormController = require('web.FormController');
    var pyUtils = require("web.py_utils");

    FormController.include({


        start: async function () {
            this.compute_active_actions()
            return this._super.apply(this, arguments)
        },


        renderButtons: function() {
            console.log('9999')
        },

        compute_active_actions: function () {

            var arch = this.renderer.arch
            var attrs = arch.attrs

            const record = this.model.get(this.handle, {raw: true});
            const context = record.getContext()

            if (attrs["edit_condition"]) {
                // eval edit condition
                try {
                    var record_data = record.data
                    var eval_context = _.extend(context, {
                        record: record_data
                    })
                    var result = pyUtils.py_eval(attrs["edit_condition"], eval_context);
                    if (!result) {
                        this.activeActions['edit'] = false
                    }
                } catch (e) {
                    console.error("Could not eval edit condition", e);
                }
            }

            if (attrs["delete_condition"]) {
                try {
                    var record_data = record.data
                    var eval_context = _.extend(context, {
                        record: record_data
                    })
                    var result = pyUtils.py_eval(attrs["delete_condition"], eval_context);
                    if (!result) {
                        this.activeActions['delete'] = false
                    }
                } catch (e) {
                    console.error("Could not eval delete condition", e);
                }
            }

            if (attrs["create_condition"]) {
                try {
                    var record_data = record.data
                    var eval_context = _.extend(context, {
                        record: record_data
                    })
                    var result = pyUtils.py_eval(attrs["create_condition"], eval_context);
                    if (!result) {
                        this.activeActions['create'] = false
                    }
                } catch (e) {
                    console.error("Could not eval create condition", e);
                }
            }

            if (this.$buttons) {
                this.$buttons.remove();
                this.$buttons = undefined;
            }
        },

         update(params, options = {}) {
            this.activeActions = this.originActiveActions;
            this.compute_active_actions();
            var self = this;
            return this._super.apply(this, arguments)
        },
    });
})
