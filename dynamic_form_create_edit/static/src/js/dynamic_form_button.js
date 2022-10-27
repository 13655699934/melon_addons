odoo.define('dynamic_form_button', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({
        updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.$buttons && this.mode === 'readonly') {
                var self = this;
                var attrs = this.renderer.arch.attrs;
                var action_edit = ['edit','create'];
                _.each(action_edit, function (action) {
                    var expr = attrs['condition_' + action];
                    if (expr){
                       var v= self._evalExpression(expr);
                       self.$buttons.find('.o_form_button_' + action).toggleClass('o_hidden', v);
                    }
                });
            }
        },
        _evalExpression: function (expr) {
            var tokens = py.tokenize(expr);
            var tree = py.parse(tokens);
            var eval_context = this.renderer.state.evalContext
            var expr_eval = py.evaluate(tree, eval_context)
            return py.PY_isTrue(expr_eval);
        }
    });
});
