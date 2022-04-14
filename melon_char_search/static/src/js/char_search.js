odoo.define('char_search.main', function (require) {
    "use strict";
    var core = require('web.core');
    var basicFields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

    var FieldChar = basicFields.FieldChar;
    var _t = core._t;
    var _lt = core._lt;
    var qweb = core.qweb;


    var FieldCharSearch = FieldChar.extend({
        xmlDependencies: ['/melon_char_search/static/src/xml/base.xml'],
        events: _.extend({}, FieldChar.prototype.events, {
            'keyup': '_onKeyup',
        }),
        _onKeyup: function (e) {
            if (this.$dropdown) {
                this.$dropdown.remove();
                this.$dropdown = undefined;
            }
            switch (e.which) {
                case $.ui.keyCode.ESCAPE:
                    //阻止默认的点击事件执行
                    e.preventDefault();
                    break;
                case $.ui.keyCode.ENTER:
                    e.preventDefault();
                    break;
            }
            this.select_items = [];
            this.result_shown = false;
            this.offset = 0;
            //获取当前输入框的值
            this.do_search(this.$input.val());
        },
        do_search: function (value) {
            var self = this;
            var context = this.attrs.context;
            if (context) {
                context = JSON.parse(context);
            } else {
                context = {};
            }
            var url = context.url;
            var model = context.model;
            var domain = context.domain;
            var pages = context.pages;
            var search_fields = context.search_fields;
            //获取到要展示的数据
            var str_field = context.fields;
            var fields = str_field.split(',');
            console.log('------------------');
            //这是请求的数据
            var post_data = {
                "model": model,
                "search_fields": search_fields,
                "fields": fields,
                "domain": domain,
                "query":value,
                "pages": pages
            }
            $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(post_data),
                dataType: 'json',
                contentType: 'application/json',
                success: function (data) {
                    //concat() 方法用于连接两个或多个数组
                    self.select_items = self.select_items.concat(data.result.data);
                    //偏移设置，为滚动加载设置参数
                    self.offset = self.offset + data.result.data.length;
                    if (!self.result_shown) {
                        self.show_dropdown();
                        self.result_shown = true;
                    } else {
                        self.$dropdown.append(qweb.render('char_search.dropdown.items', {
                            select_items: data.result.data,
                            fields: fields,
                        }));
                    }
                    //当点击数据后，执行数值赋值功能
                    self.$dropdown.find('a').click(function (ev) {
                        ev.preventDefault();
                        //获取当前选择的index
                        var select_index = $(ev.currentTarget).data('index');
                        if (!select_index) {
                            return
                        }
                        //根据select_index获取到记录
                        var select_item = self.select_items.filter(function (item) {
                            return item.id == select_index
                        });
                        //因为字段个数不固定，所以循环取值赋值
                        for (var i = 0; i < fields.length; i++) {
                            var field = fields[i];
                            var all_fields = self.getParent().allFieldWidgets[self.dataPointID];
                            var field_item = all_fields.filter(function (f) {
                                return f.name == fields[i]
                            });
                            if (field_item.length) {
                                field_item[0]._setValue(select_item[0][field]);
                                field_item[0].$input.val(select_item[0][field]);
                            }
                        }
                        //赋值给当前选择的文本框，$(ev.currentTarget).data('value')获取当前选择的数据的值
                        self.$input.val($(ev.currentTarget).data('value'));
                        //值附上后，隐藏框子
                        self.$dropdown.hide();
                    });
                },
            });

        },
        show_dropdown: function () {
            var self = this;
            //将从接口里面获取的数据展示到qweb上面
            this.$dropdown = $(qweb.render('char_search.dropdown', {
                select_items: this.select_items,
            }));
            this.$dropdown.appendTo($('body'));
            //offset() 方法设置或返回被选元素相对于文档的偏移坐标。
            this.$dropdown.offset({top: this.$el.offset().top - 75, left: this.$el.offset().left});
            //jquery .show()显示被选的元素 ,hide() 隐藏被选的元素
            this.$dropdown.show();
            //scroll 事件适用于所有可滚动的元素
            this.$dropdown.scroll(function (ev) {
                if (($(this)[0].scrollTop + $(this).height() + 12) >= $(this)[0].scrollHeight) {
                    self.do_search();
                }
            });
        },
        init: function () {
            this._super.apply(this, arguments);
            this.select_items = [];
            this.result_shown = false;
            this.offset = 0;
        },
        //作用是鼠标移走 光标移走后，隐藏展示的框
        _renderEdit: function () {
            this._super.apply(this, arguments);
            var self = this;
        //当元素（或在其内的任意元素）失去焦点时发生 focusout 事件
            this.$input.focusout(function (ev) {
                if (self.$dropdown) {
                    if (!$(ev.relatedTarget).hasClass('dropdown-item')) {
                        self.$dropdown.hide();
                    }
                }
            });
        }
    });

    field_registry.add('melon_char_search', FieldCharSearch);
    return FieldCharSearch;

});