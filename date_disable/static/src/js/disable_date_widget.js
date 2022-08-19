odoo.define('date_disable.disable_date_widget', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var FieldDate = require('web.basic_fields').FieldDate;
    var datepicker = require('web.datepicker');

    var section_date = FieldDate.extend({
        _makeDatePicker: function () {
            let newDate = moment();
            this.datepickerOptions['minDate'] = moment({Y:newDate.year(), M:newDate.month(), d:newDate.date()});
            return new datepicker.DateWidget(this, this.datepickerOptions);
        },
    })

    // 注册名称为disable_date_widget的widget
    registry.add('disable_date_widget', section_date);


});