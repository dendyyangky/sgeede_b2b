odoo.define('sgeede_pos_list.screens', ['point_of_sale.screens'], function (require) {
"use strict";
    var screens = require('point_of_sale.screens');

    screens.ProductListWidget.include({
        renderElement: function() {
            var self = this;
            this._super();

            $.fn.replaceWithPush = function(elem) {
                var $elem = $(elem);
                this.replaceWith($elem);
                return $elem;
            };

            var el_node = this.el;
            if(this.pos.config.is_list_view) {
                var list_container = el_node.querySelector('.product-list');
                
                $(list_container).find('.product-col').filter(function() {
                    $(this).replaceWith($('<td>' + this.innerHTML + '</td>'));
                })
                $(list_container).find('.product-row').filter(function() {
                    var row = $(this).replaceWithPush($('<tr data-product-id="' + $(this).data('product-id') + '">' + this.innerHTML + '</tr>'));
                    row[0].addEventListener('click', self.click_product_handler);
                })
            }
        }
    });
});