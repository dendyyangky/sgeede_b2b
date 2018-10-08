odoo.define('sgeede_date_range.search_filters', function (require) {
"use strict";

var core = require('web.core');
var datepicker = require('web.datepicker');
var formats = require('web.formats');
var Widget = require('web.Widget');

var _t = core._t;
var _lt = core._lt;

//getting the original search filters on web module
var searchfilter = require('web.search_filters');

    
//extending widget
    searchfilter.ExtendedSearchProposition.include({
        operator_changed: function (e) {
        var $value = this.$('.searchview_extended_prop_value');
        switch ($(e.target).val()) {
        case '∃':
        case '∄':
            $value.hide();
            break;
        case 'between':
            $value.show();
            this.value.show_inputs($(e.target));
            break;
        default:
            $value.show();
            $value.find(".o_datepicker:not(:first-child)").hide();
            //hide the second input field
        }
        },
        get_filter: function () {
        if (this.attrs.selected === null || this.attrs.selected === undefined)
            return null;
        var field = this.attrs.selected,
            op_select = this.$('.searchview_extended_prop_op')[0],
            operator = op_select.options[op_select.selectedIndex];

        return {
            attrs: {
                //remove [] on the domain
                domain: this.value.get_domain(field, operator),
                string: this.value.get_label(field, operator),
            },
            children: [],
            tag: 'filter',
        };
        },
    });

   searchfilter.ExtendedSearchProposition.DateTime.include({
    	operators: [
            {value: "=", text: _lt("is equal to")},
            {value: "!=", text: _lt("is not equal to")},
            {value: ">", text: _lt("greater than")},
            {value: "<", text: _lt("less than")},
            {value: ">=", text: _lt("greater than or equal to")},
            {value: "<=", text: _lt("less than or equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")},
            {value: "between", text: _lt("is between")}
        ],
        show_inputs: function ($operator) {
            if ($operator.val() === 'between') {
                if (!this.datewidget_2) {
                    this.datewidget_2 = new (this.widget())(this);
                    this.datewidget_2.appendTo(this.$el);
                    return this.datewidget_2
                }
                else {
                    this.datewidget_2.$el.show();
                }
            }
            else {
                if (this.datewidget_2) {
                    this.datewidget_2.$el.hide();
                }
            }
        },
        toStringBetween: function () {
            var str = formats.format_value(this.get_value(), { type:this.attributes['type'] });
            if (this.datewidget_2 && this.datewidget_2.get_value()) {
                str += ' and ' + formats.format_value(this.datewidget_2.get_value(), { type:this.attributes['type'] });
            }
            return str
        },

        format_label: function (format, field, operator) {
            if (operator.value === "between") {
                //use the custom label if the operator is between
                //same problem as odoo8
                var between_label = this.toStringBetween()
                console.log(between_label)
                return _.str.sprintf(format, {
                    field: field.string,
                    operator: operator.label || operator.text,
                    value: between_label
                });
            } else {
                return _.str.sprintf(format, {
                    field: field.string,
                    // According to spec, HTMLOptionElement#label should return
                    // HTMLOptionElement#text when not defined/empty, but it does
                    // not in older Webkit (between Safari 5.1.5 and Chrome 17) and
                    // Gecko (pre Firefox 7) browsers, so we need a manual fallback
                    // for those
                    operator: operator.label || operator.text,
                    value: this
                });
            }
        },
    });

    searchfilter.ExtendedSearchProposition.Field.include({
        get_domain: function (field, operator) {
        switch (operator.value) {
        case '∃': return this.make_domain(field.name, '!=', false);
        case '∄': return this.make_domain(field.name, '=', false);
        case 'between': return [[field.name, '>=', this.datewidget.get_value()], [field.name,'<=', this.datewidget_2.get_value()]];// add extra case here for between
        default: return this.make_domain(
            field.name, operator.value, this.get_value());
            }
        },
        make_domain: function (field, operator, value) {
            return [[field, operator, value]];//add [] on the return
        },
    });

    return {
    ExtendedSearchProposition: searchfilter
    };
});