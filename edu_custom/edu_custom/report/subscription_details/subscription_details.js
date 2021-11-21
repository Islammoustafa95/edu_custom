// Copyright (c) 2016, Hardik Gadesha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Subscription Details"] = {
	"filters": [
		{
			"fieldname":"plan",
			"label": __("Subscription Name"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Subscription Plan",
		},
		{
			"fieldname":"from_date",
			"label": __("Subscription Start Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("Subscription End Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.month_end()
		},
		{
			"fieldname":"instructor",
			"label": __("Instructor"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Instructor",
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Customer",
		},
	]
};
