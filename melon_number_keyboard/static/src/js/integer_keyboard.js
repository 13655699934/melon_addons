odoo.define('integer_number_keyboard.main', function (require) {
    "use strict";
    var core = require('web.core');
    var basicFields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

    var FieldInteger = basicFields.FieldInteger;
    var _t = core._t;
    var _lt = core._lt;
    var qweb = core.qweb;

    var FieldIntegerSearch = FieldInteger.extend({
        xmlDependencies: ['/melon_number_keyboard/static/src/xml/base.xml'],
        events: _.extend({}, FieldInteger.prototype.events, {
            'keyup': '_onKeyup',
        }),
        _onKeyup: function (e) {
        },
        init: function () {
            this._super.apply(this, arguments);
            this.select_items = [];
            this.result_shown = false;
            this.offset = 0;
        },
        show_dropdown: function () {
            var self = this;
            //将从接口里面获取的数据展示到qweb上面
            if (self.$dropdown) {
                self.$dropdown.remove();
            }
            if ($("#drop_float_keyboard")){
               $("#drop_float_keyboard").remove()
            }
            this.$dropdown = $(qweb.render('integer_keyboard', {
                select_items: this.select_items,
            }));
            var is_hide = 'false'
            this.$dropdown.appendTo($('body'));
            //offset() 方法设置或返回被选元素相对于文档的偏移坐标。
            this.$dropdown.offset({top: this.$el.offset().top - 75, left: this.$el.offset().left});
            //jquery .show()显示被选的元素 ,hide() 隐藏被选的元素
            this.$dropdown.show();
            var result_value = '';
            //当点击数据后，执行数值赋值功能
            self.$dropdown.find('input').click(function (ev) {
                ev.preventDefault();
                //获取当前选择的index
                if ($(ev.currentTarget)[0].value === 'x') {
                    result_value = result_value.substring(0, result_value.length - 1);
                } else {
                    result_value = result_value + $(ev.currentTarget)[0].value
                }
                //赋值给当前选择的文本框，$(ev.currentTarget).data('value')获取当前选择的数据的值
                self.$input.val(result_value);
                self._setValue(result_value)
                is_hide = 'false'
            });
            //点空白处值附上后，隐藏框子
            $("#drop_int_keyboard").onclick = function () {
                is_hide = 'false'
            };
            document.onclick = function () {
                console.log('=============')
                if (is_hide === 'true') {
                     self.$dropdown.remove();
                }
                is_hide = 'true';
            }
        },

        //作用是鼠标移走 光标移走后，隐藏展示的框
        _renderEdit: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$input.focus(function (ev) {
                self.show_dropdown()
            });
        }
    });

    field_registry.add('integer_number_keyboard', FieldIntegerSearch);
    return FieldIntegerSearch;

});