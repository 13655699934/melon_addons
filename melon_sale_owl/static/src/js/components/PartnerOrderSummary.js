/** @odoo-module */
odoo.define("melon_sale_owl.PartnerOrderSummary", function (require) {
    'use strict'
    const FormRenderer = require("web.FormRenderer");
    const {Component} = owl;
    const { useState } = owl.hooks;
    import { ComponentWrapper } from "web.OwlCompatibility";


    class PartnerOrderSummary extends Component {
         partner = useState({});
         constructor(self, partner) {
             super();
             this.partner = partner;
         }

    };

    Object.assign(PartnerOrderSummary, {
        template: "melon_sale_owl.PartnerOrderSummary"
    });

    FormRenderer.include({
        async _renderView() {
            await this._super(...arguments);
            for(const element of this.el.querySelectorAll(".o_partner_order_summary")) {
             this._rpc({
                 model: "res.partner",
                 method: "read",
                 args: [[this.state.data.partner_id.res_id]]
             }).then(data => {
                 (new ComponentWrapper(
                     this,
                     PartnerOrderSummary,
                     useState(data[0])
                 )).mount(element);
             });
        }
        }

    });


});