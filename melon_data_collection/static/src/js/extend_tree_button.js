odoo.define('melon_data_collection.tree_view_button', function (require) {
    "use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var session = require('web.session');
    var rpc = require('web.rpc');

    var qweb = core.qweb;
    //数据采集
    var AddListViewController = ListController.extend({
        buttons_template: 'MinfoAddsListView.buttons',
        /**
         * Extends the renderButtons function of ListView by adding an event listener
         * on the bill upload button.
         *
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            this._super.apply(this, arguments);
            var self = this;
            var company_id = session.company_id;
        },
        renderButtons: function () {
            this._super.apply(this, arguments); // Possibly sets this.$buttons
            if (this.$buttons) {
                var self = this;
                this.$buttons.on('click', '.o_button_add_tree_btn_import_info', function () {
                    var active_ids = [];
                    var select_value = $('tbody .o_list_record_selector input');
                    var state = self.model.get(self.handle, {raw: true});                    //这里是获取列表中选中的record
                    for (var i = 0; i < select_value.length; i++) {
                        if (select_value[i].checked === true) {
                            active_ids.push(state.res_ids[i]);
                        }
                    }
                    self.do_action({
                        type: 'ir.actions.act_window',
                        res_model: 'import.talent.info.wizard',//向导模型
                        target: '数据采集',
                        views: [[false, 'form']],
                        context: {
                            active_ids: active_ids,
                        },
                    });
                });
            }
        }
    });
    var AddsListView1 = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: AddListViewController,
        }),
    });

    viewRegistry.add('add_buttons_tree', AddsListView1);
});