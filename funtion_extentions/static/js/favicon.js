/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "web.utils";

patch(WebClient.prototype, "funtion_extentions.WebClient", {
    setup() {
        this._super();
        this.title.setParts({ zopenerp: "InsurAdmin" });
    },
});