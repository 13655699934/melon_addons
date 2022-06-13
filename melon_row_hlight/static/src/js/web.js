odoo.define('melon_row_hlight.web', function (require) {
    "use strict";

    var ListRenderer = require("web.ListRenderer");
    var session = require('web.session');
    var rpc = require('web.rpc');

    ListRenderer.include({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.model = model;
            this.renderer = renderer;
        },
        _onRowClicked: function (event) {
            if (!window.getSelection().toString() && !event.ctrlKey) {
                this._super.apply(this, arguments);
            }
            var recordId = $(event.currentTarget).data('id');
            var record = this._findRecordById(recordId);
            var res_id = record.res_id;
            if (this.model.model === 'watermark.design.order') {
                var company_id = session.company_id;
                var vals = [res_id];
                var result = rpc.query({
                    model: 'watermark.design.order',
                    method: 'set_value',
                    args: [res_id, vals],
                }).then(function (result) {
                    console.log('---------' + result);
                });
                console.log(session.uid);
                console.log(session.company_id);
            }
        },

        _findRecordById: function (id) {
            return _.find(this.state.data, function (record) {
                return record.id === id;
            });
        },
        _onSelectRecord: function (event) {
            var self = this;
            this._super.apply(this, arguments);
            var checkbox = $(event.currentTarget).find('input');
            var $selectedRow = $(checkbox).closest('tr')
            if ($(checkbox).prop('checked')) {
                $selectedRow.addClass('row_selected');
            } else {
                $selectedRow.removeClass('row_selected')
            }
        },
        _onToggleSelection: function (event) {
            this._super.apply(this, arguments);
            var checked = $(event.currentTarget).prop('checked') || false;
            if (checked) {
                this.$('tbody .o_list_record_selector').closest('tr').addClass('row_selected')
            } else {
                this.$('tbody .o_list_record_selector').closest('tr').removeClass('row_selected')
            }
        },
    });
});