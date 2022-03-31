odoo.define('melon_iframe_largescreen',function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.AbstractAction');


    var HomePagename_tag_big_data =Widget.extend({template: "templates_big_data",});
    core.action_registry.add('tag_big_data',HomePagename_tag_big_data);

    var HomePagename_smart_logistic =Widget.extend({template: "templates_smart_logistics",});
    core.action_registry.add('tag_smart_logistic',HomePagename_smart_logistic);


});