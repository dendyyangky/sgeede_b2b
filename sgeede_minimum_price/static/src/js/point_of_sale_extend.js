odoo.define('sgeede_minimum_price.point_of_sale_extend', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var _t = core._t;
// they created function to add fields now
	models.load_fields("product.product", "minimum_price");

// function to validate minimum price in pos
	screens.PaymentScreenWidget.include({
		validate_order: function(force_validation){
			var self = this;
			var order = this.pos.get_order();

			var orderlines = order.get_orderlines();
			if (orderlines.length > 0){
				for(var i = 0; i < orderlines.length; i++){
					var line = orderlines[i];
					var base_price = line.get_base_price();
					var minimum_price = line.product["minimum_price"] * line.quantity;
					if (base_price < minimum_price){
						this.gui.show_popup('error',{
							'message': _t('Price is lower than the minimum product price!'),
							'body': _t("Please recheck ") + line.product["display_name"],
						});
					return false;
					}
				}
			}
		this._super(); 
		}
	});
});