odoo.define('melon_btn_search.btn_search', function (require) {
"use strict";
var core = require('web.core');
var widgetRegistry = require('web.widget_registry');
var Widget = require('web.Widget');
var Dialog = require('web.Dialog');

var _t = core._t;
var _lt = core._lt;
var qweb = core.qweb;


var BtnSearch = Widget.extend({
    template: 'melon_btn_search.btn_search',
    xmlDependencies: ['/melon_btn_search/static/src/xml/base.xml'],
    events: {
        'click .o_btn_search': 'open_dialog',
    },
    open_dialog: function (ev) {
        var self = this;
        ev.preventDefault();
        ev.stopPropagation();
        var content = '<div><input id="keyword"/><button class="melon_btn" id="search_button">搜索</button><div id="result" style="height: 300px;overflow-y: scroll;"></div></div>';
        this.$content = $(content);
        var fields = ['name','email'];
        this.$content.find('#search_button').click(function(){
            self.result_shown = false;
            self.select_items = [];
            self.offset = 0;
            self.$content.find('tbody tr').remove();
            self.do_search();
        });
       var $result = self.$content.find('#result');
       $result.scroll(function(ev) {
            if (($(this)[0].scrollTop + $(this).height()) >= $(this)[0].scrollHeight) {
                self.do_search();
            }
        });
        var options = {
            title: 'Search ..',
            $content: this.$content,
            buttons: [{
                text: '确认',
                classes: 'btn-primary melon_btn',
                close: true,
                click: function(ev) {
                    var select_items = self.$content.find('input:checked');
                    if (!select_items.length) {return}
                    var name_list = [];
                    for (var i=0;i<select_items.length;i++) {
                        var select_index = $(select_items[i]).data('index');
                        var select_item = self.select_items.filter(function(item){return item.id==select_index});
                        name_list.push(select_item[0].name);
                    }
                    var name = name_list.join(',');
                    var all_fields = self.getParent().allFieldWidgets[self.record_id];
                    var field_item = all_fields.filter(function(f){
                        console.log('----f.name--------'+f.name);
                        return f.name=='name'
                    });
                    if (field_item.length) {
                        field_item[0]._setValue(name);
                        // field_item[0].$input.val(name);
                        // field_item[0].$input.value(name);
                    }
                }
            }, {
                text: _t('取消'),
                close: true,
            }],
        };
        this.dialog = new Dialog(this, options);
        this.dialog.open();
   },
    init: function (parent, data, options) {
        this._super.apply(this, arguments);
        this.record_id = data.id;
        var options = options.attrs.options;
        if (options) {
            options = JSON.parse(options);
        }
        this.options = options || {};
        this.select_items = [];
        this.result_shown = false;
        this.offset = 0;
    },
    do_search: function() {
        var self = this;
        var keyword = this.$content.find('#keyword').val();
        var url = 'http://127.0.0.1:8099/web/dataset/call_kw/res.partner/search_read';
        // var url = self.options.url;
        var postdata = {
                "domain": "domain",
            }
        var domain = [
            '|',
            ['name', 'ilike',keyword],
            ['email', 'ilike',keyword],
        ];
        var field_str=self.options.fields
        var fields = field_str.split(',')
        var limit = 10;
        var order = 'name';
        var params = {
            id: 207163797,
            jsonrpc: "2.0",
            method: "call",
            params: {
                "args": [],
                "model": "res.partner",
                "method": "search_read",
                "kwargs": {
                "domain": domain,
                "fields": fields,
                "offset": self.offset,
                "limit": limit,
                "order": order
              }
            }
        };
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(params),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                self.select_items = self.select_items.concat(data.result);
                self.offset = self.offset + data.result.length;
                if (!self.result_shown) {
                    self.$content.find('#result').html(qweb.render('melon_btn_search.btn_search_result', {
                        select_items: self.select_items,
                        fields: fields,
                    }));
                    self.result_shown = true;
                } else {
                    self.$content.find('#result tbody').append(qweb.render('melon_btn_search.btn_search_result.lines', {
                        select_items: data.result,
                        fields: fields,
                    }));
                }

            },
        });
    }
});

widgetRegistry.add('melon_btn_search', BtnSearch);

return BtnSearch;

});