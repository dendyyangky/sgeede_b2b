odoo.define('sgeede_pos_lock.popups', ['point_of_sale.popups', 'point_of_sale.gui', 'web.rpc'], 
    function (require) {
"use strict";
    var popups = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var rpc = require('web.rpc');

    var LockScreenPopupWidget = popups.extend({
        template: 'LockScreenPopupWidget',
        show: function(options){
            options = options || {};
            this._super(options);

            this.renderElement();
            this.$('input').focus();
        },
        click_confirm: function(){
            var self = this;
            var value = this.$('input').val();

            if(value) {
                rpc.query({
                    model: 'res.users',
                    method: 'authenticate',
                    args: [self.pos.attributes.db, self.pos.attributes.username, value, false],
                }).then(function(uid){
                    if(uid) {
                        self.gui.close_popup();
                    } else {
                        self.$('.error').html('Password didn\'t match with current user')
                    }
                });
            } else {
                self.$('.error').html('Please enter your password')
            }
        },
    });
    gui.define_popup({name:'lockscreen', widget: LockScreenPopupWidget});
});