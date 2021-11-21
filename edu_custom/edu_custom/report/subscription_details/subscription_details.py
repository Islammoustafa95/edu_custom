# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr
from frappe.desk.reportview import build_match_conditions
from collections import defaultdict

def execute(filters=None):
	if not filters:
		filters = {}

	conditions = get_conditions(filters)
	data = []
	columns = get_column()

	# d.plan,s.name,s.start,s.subscription_end_date,s.instructor,s.customer
	data = frappe.db.sql("""select * from `tabSubscription` s inner join `tabSubscription Plan Detail` d on s.name = d.parent
		where 1=1 %s"""%(conditions),filters, as_dict=1,debug=True)

	for i in data:
		# frappe.msgprint(cstr(i.get('plan')))
		# frappe.msgprint(cstr(i))
		# frappe.msgprint(cstr(i.sname) + cstr(i.start))
		row={}
		# row["plan"] = i.plan
		row["plan"] = i.get('plan')
		row["subscription"] = i.get('name')
		row["from_date"] = i.get('start')
		row["to_date"] = i.get('subscription_end_date')
		row["instructor"] = i.get('instructor')
		row["customer"] = i.get('customer')
		data.append(row)	

	return columns , data

def get_conditions(filters):
	conditions = ""
	if filters.get("plan"):
		filters.plan = filters.get('plan')
		conditions += " and d.plan = %(plan)s"
	if filters.get("from_date"):
		filters.from_date = filters.get('from_date')
		conditions += " and s.start >= %(from_date)s"
	if filters.get("to_date"):
		filters.to_date = filters.get('to_date')
		conditions += " and s.subscription_end_date <= %(to_date)s"
	if filters.get("instructor"):
		filters.instructor = filters.get('instructor')
		conditions += " and s.instructor = %(instructor)s"
	if filters.get("customer"):
		filters.customer = filters.get('customer')
		conditions += " and s.customer = %(customer)s"

	return conditions

def get_column():
	columns = [
		{
			"fieldname": "plan",
			"label": _("Subscription Name"),
			"fieldtype": "Link",
			"options": "Subscription Plan",
			"width": 150,
		},
		{
			"fieldname": "subscription",
			"label": _("Subscription"),
			"fieldtype": "Link",
			"options": "Subscription",
			"width": 150,
		},
		{
			"fieldname": "from_date",
			"label": _("Subscription Start Date"),
			"fieldtype": "Date",
			"width": 150,

		},
		{
			"fieldname": "to_date",
			"label": _("Subscription End Date"),
			"fieldtype": "Date",
			"width": 150,

		},
		{
			"fieldname": "instructor",
			"label": _("Instructor"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Data",
			"width": 150,
		},
	]

	return columns

# def get_master(conditions, filters):
# 	master = {}
# 	qty = {}
# 	data = frappe.db.sql("""select item_code,c.item_name, c.uom from `tabStock Entry` p inner join `tabStock Entry Detail` c on p.name = c.parent
# 		where p.docstatus = 1 %s group by 1 order by 1"""%(conditions), filters, as_dict=1)

# 	return data
