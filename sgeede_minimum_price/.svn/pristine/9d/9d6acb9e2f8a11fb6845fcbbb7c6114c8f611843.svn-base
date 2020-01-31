odoo.define('sgeede_minimum_price.point_of_sale_extend', function (require) {
	"use strict";
	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var _t = core._t;

	//including the field of of minimum_price
	models.load_fields("product.product", "minimum_price");

	//adding check_min_price before validate
	screens.PaymentScreenWidget.include({
		check_min_price: function(force_validation){
			var self = this;
			var order = this.pos.get_order();

			var orderlines = order.get_orderlines();
			if (orderlines.length > 0){
				for(var i = 0; i < orderlines.length; i++){
					var orderline = orderlines[i];
					var base_price = orderline.get_base_price();
					var minimum_price = orderline.quantity * orderline.product["minimum_price"];
					if(base_price < minimum_price){
						this.gui.show_popup('error', {
							'title': _t('Price is lower than the minimum product price!'),
							'body': _t('Please recheck ') + orderline.product["display_name"],
						});
						return false;
					}
				}
			}
			return true
		},

		validate_order: function(force_validation){
			if (this.check_min_price(force_validation)) {
			this._super(force_validation);
			}
		},
	});
});