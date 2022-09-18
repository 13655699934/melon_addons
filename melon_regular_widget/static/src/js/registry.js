odoo.define('melon_regular_widget.registry', function (require) {
"use strict";

var registry = require('web.field_registry');
var inputMask = require('melon_regular_widget.fields');

registry
    .add('mask', inputMask.FieldMask)
    .add('regex_mask', inputMask.FieldRegexMask);
});