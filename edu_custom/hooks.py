# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "edu_custom"
app_title = "Edu Custom"
app_publisher = "Codes Soft"
app_description = "Education Customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shahid@codessoft.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/edu_custom/css/edu_custom.css"
# app_include_js = "/assets/edu_custom/js/edu_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/edu_custom/css/edu_custom.css"
# web_include_js = "/assets/edu_custom/js/edu_custom.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "edu_custom.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "edu_custom.install.before_install"
# after_install = "edu_custom.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "edu_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Subscription": {
		"validate": "edu_custom.doctype_changes.subscription_validate",
		"after_insert" : "edu_custom.doctype_changes.subscription_after_insert"
	},
	"Student": {
		"validate": "edu_custom.doctype_changes.student_validate",
	},
	"Sales Invoice": {
		"validate": "edu_custom.doctype_changes.sales_invoice_validate",
	},
}

scheduler_events = {
	"daily_long": [
		"edu_custom.doctype_changes.cancel_subscription_on_expiry",
		"edu_custom.doctype_changes.subscription_alerts",
	],
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"edu_custom.tasks.all"
# 	],
# 	"daily_long": [
# 		"edu_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"edu_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"edu_custom.tasks.weekly"
# 	]
# 	"monthly": [
# 		"edu_custom.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "edu_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "edu_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "edu_custom.task.get_dashboard_data"
# }

