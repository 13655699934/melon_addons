odoo.define('date_disable.disable_datetime_widget', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var FieldDateTime = require('web.basic_fields').FieldDateTime;
    var datepicker = require('web.datepicker');
    var section_datetime = FieldDateTime.extend({
        _makeDatePicker: function () {
            const format = "YYYY-MM-DD HH:mm:ss";
            this.datepickerOptions['minDate'] = moment().format(format);
            return new datepicker.DateTimeWidget(this, this.datepickerOptions);
        },
    })

    // 注册名称为disable_datetime_widget的widget
    registry.add('disable_datetime_widget', section_datetime);


});