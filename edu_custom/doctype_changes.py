import frappe
from frappe.auth import LoginManager

from frappe import utils
import datetime
from frappe.core.doctype.sms_settings.sms_settings import send_sms
import json
from frappe.utils.background_jobs import enqueue
from datetime import date, datetime, timedelta
import requests
# from erpnext.accounts.doctype.subscription.subscription import cancel_subscription


def subscription_validate(self, method):
	check = frappe.db.get_value("Student", {"customer": self.customer}, "name")
	if not check:
		check_email = frappe.db.get_value("Customer", self.customer, "email_id")
		# if not check_email:
		# 	frappe.throw("Please enter customer email, as it is required for creating student.")
		doc = frappe.new_doc("Student")
		doc.first_name = self.customer
		doc.customer = self.customer
		doc.instructor = self.instructor
		doc.student_email_id = check_email
		doc.student_mobile_number = frappe.db.get_value("Customer", self.customer, "mobile_no")
		doc.flags.ignore_mandatory=True
		doc.insert(ignore_permissions=True)
	else:
		frappe.db.set_value("Student", check, "instructor", self.instructor)


@frappe.whitelist(allow_guest=True)
def get_ratings(instructor=None, student_id=None):
	cond = ""
	if student_id:
		cond += " and student = '{}'".format(student_id)
	if instructor:
		cond += " and instructor = '{}'".format(instructor)
	return frappe.db.sql("select * from `tabStudent Rating` where 1=1 {}".format(cond), as_dict=1)

@frappe.whitelist(allow_guest=True)
def get_attendance(instructor=None, student_id=None):
	if student_id:
		customer = frappe.db.get_value("Student", {"name": student_id}, "customer")
		status = frappe.db.get_value("Subscription", {"customer": customer}, "status")
		if status != "Active": return "No Active Subscription"
	cond = ""
	if student_id:
		cond += " and student = '{}'".format(student_id)
	if instructor:
		cond += " and instructor = '{}'".format(instructor)
	return frappe.db.sql("select * from `tabStudent Attendance` where 1=1 {}".format(cond), as_dict=1)

@frappe.whitelist(allow_guest=True)
def create_student_rating(student_id, date, title, rating):
	doc = frappe.new_doc("Student Rating")
	doc.student = student_id
	doc.date = frappe.utils.getdate(date)
	doc.title = title
	doc.rating = rating
	doc.flags.ignore_mandatory=True
	doc.insert(ignore_permissions=True)
	return doc

@frappe.whitelist(allow_guest=True)
def login_instructor(usr, pwd):
	login_manager = LoginManager()
	login_manager.authenticate(usr,pwd)
	login_manager.post_login()
	if frappe.response['message'] == 'Logged In':
		instructor = frappe.db.get_value("Instructor", {"user": login_manager.user}, "name")
		if instructor: return instructor
	return "No Instructor Found."

def student_validate(self, method):
	from ummalqura.hijri_date import HijriDate
	self.other_date=""
	if self.date_of_birth:
		date = frappe.utils.getdate(self.date_of_birth)
		um = HijriDate(date.year, date.month, date.day, gr=True)
		self.other_date = str(um.year)+"/"+str(um.month)+"/"+str(um.day_gr)

	from pathlib import Path
	import shutil
	import pyqrcode
	url = "http://167.71.142.98/"
	data = url+"attendance?student_id="+self.name
	name_to_be = "QRCode"+self.name+".png"
	try:
		# qr = pyqrcode.create(data)
		# qr.svg(name_to_be, scale=2, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
		big_code = pyqrcode.create(data)
		big_code.png(name_to_be, scale=6, module_color=[255, 255, 255], background=[251,97,63])
		shutil.move("/home/frappe/frappe-bench/sites/"+name_to_be, '/home/frappe/frappe-bench/sites/site1.local/public/files/barcodes/'+name_to_be)
	except Exception as e:
		error_message = frappe.get_traceback()+"Error \n"+str(e)
		frappe.log_error(error_message, "QR Code Error")

def sales_invoice_validate(self, method):
	generate_qr_for_print(self.doctype, self.name, "Invoice QR")

def generate_qr_for_print(doctype, name, print_format):
	from pathlib import Path
	import shutil
	import pyqrcode
	url = "http://167.71.142.98/"
	data = url+"printview?doctype={}&name={}&trigger_print=1&format={}&no_letterhead=0&_lang=ar".format(doctype, name, print_format)
	name_to_be = "QRCode"+name+".png"
	try:
		# qr = pyqrcode.create(data)
		# qr.svg(name_to_be, scale=2, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
		big_code = pyqrcode.create(data)
		big_code.png(name_to_be, scale=6)
		shutil.move("/home/frappe/frappe-bench/sites/"+name_to_be, '/home/frappe/frappe-bench/sites/site1.local/public/files/barcodes/'+name_to_be)
	except Exception as e:
		error_message = frappe.get_traceback()+"Error \n"+str(e)
		frappe.log_error(error_message, "QR Code Error")

@frappe.whitelist()
def send_outstanding_notifications(student_id=None, student_name=None, mobile=None):
	
	if student_id and student_name and mobile:
		url = "http://167.71.142.98/printview?doctype=Student&name={}&trigger_print=1&format=Card A4&no_letterhead=0&_lang=en".format(student_id)
		# import bitly_api
		API_USER = "shahid03351206668@gmail.com"
		API_KEY = "05e3f667ef7ed0b538c4a5da12a62fbaebfacb15"
		headers = {
		    "content-type": "application/json", 
		    "Authorization": "Bearer 05e3f667ef7ed0b538c4a5da12a62fbaebfacb15"
		}

		body = json.dumps({
		  "domain": "bit.ly",
		  "long_url": url
		})

		URL = "https://api-ssl.bitly.com/v4/shorten"
		res = requests.post(url = URL, data = body, headers = headers)
		print(res.text)
		r = json.loads(res.text)
		new_url = r.get("link")
		print(new_url)
		message = """Dear {}, please visit the link below to print your card: \n {}""".format(student_name,new_url)
		# import smsutil
		# message = smsutil.encode(message)
		try:
			send_sms([mobile], message)
		except Exception as e:
			error_message = frappe.get_traceback()+"Error \n"+str(e)
			frappe.log_error(error_message, "SMS Error")

def subscription_after_insert(self, method):
	self.generate_invoice()
	sms_message = frappe.db.get_value("Subscription SMS Text", "Subscription SMS Text", "on_creation")
	mobile = frappe.db.get_value("Student", {"customer": self.customer}, "student_mobile_number")
	message = frappe.render_template(sms_message, {'doc': self})
	if message and mobile:
		try:
			send_sms([mobile], message)
		except Exception as e:
			error_message = frappe.get_traceback()+"Error \n"+str(e)
			frappe.log_error(error_message, "SMS Error")

def cancel_subscription(name):
	"""
	Cancels a `Subscription`. This will stop the `Subscription` from further invoicing the
	`Subscriber` but all already outstanding invoices will not be affected.
	"""
	subscription = frappe.get_doc('Subscription', name)
	subscription.cancel_subscription()

def cancel_subscription_on_expiry():
	now_date = frappe.utils.getdate()
	subscription = frappe.db.get_list('Subscription', fields=['*'], filters={"status": "Active"})
	if subscription:
		for d in subscription:
			if now_date == d['subscription_end_date']:
				cancel_subscription(d['name'])
				sms_message = frappe.db.get_value("Subscription SMS Text", "Subscription SMS Text", "ended")
				mobile = frappe.db.get_value("Student", {"customer": d.customer}, "student_mobile_number")
				message = frappe.render_template(sms_message, {'doc': d})
				if message and mobile:
					try:
						send_sms([mobile], message)
					except Exception as e:
						error_message = frappe.get_traceback()+"Error \n"+str(e)
						frappe.log_error(error_message, "SMS Error")

def subscription_alerts():
	now_date = frappe.utils.getdate() + timedelta(days=15)
	subscription = frappe.db.sql("""select * from `tabSubscription` where status = 'Active' and subscription_end_date = '{}'""".format(now_date))
	for d in subscription:
		sms_message = frappe.db.get_value("Subscription SMS Text", "Subscription SMS Text", "before_15_days")
		mobile = frappe.db.get_value("Student", {"customer": d.customer}, "student_mobile_number")
		message = frappe.render_template(sms_message, {'doc': d})
		if message and mobile:
			try:
				send_sms([mobile], message)
			except Exception as e:
				error_message = frappe.get_traceback()+"Error \n"+str(e)
				frappe.log_error(error_message, "SMS Error")

	now_date = frappe.utils.getdate() + timedelta(days=5)
	subscription = frappe.db.sql("""select * from `tabSubscription` where status = 'Active' and subscription_end_date = '{}'""".format(now_date))
	for d in subscription:
		sms_message = frappe.db.get_value("Subscription SMS Text", "Subscription SMS Text", "before_5_days")
		mobile = frappe.db.get_value("Student", {"customer": d.customer}, "student_mobile_number")
		message = frappe.render_template(sms_message, {'doc': d})
		if message and mobile:
			try:
				send_sms([mobile], message)
			except Exception as e:
				error_message = frappe.get_traceback()+"Error \n"+str(e)
				frappe.log_error(error_message, "SMS Error")

def test_Qr():
	import pyqrcode
	big_code = pyqrcode.create('0987654321')
	big_code.png('code.png', scale=6, module_color=[255, 255, 255], background=[251,97,63])

@frappe.whitelist()
def restart_subscription(name):
	subscription = frappe.get_doc('Subscription', name)
	if subscription.status == 'Cancelled':
		subscription.status = 'Active'
		subscription.db_set('start', utils.nowdate())
		subscription.update_subscription_period(utils.nowdate())
		subscription.invoices = []
		for d in subscription.plans:
			if d.billing_interval == "Day":
				subscription.subscription_end_date = frappe.utils.add_days(subscription.start, d.qty)
			elif d.billing_interval == "Week":
				subscription.subscription_end_date = frappe.utils.add_days(subscription.start, d.qty*7)
			elif d.billing_interval == "Month":
				subscription.subscription_end_date = frappe.utils.add_months(subscription.start, d.qty)
			elif d.billing_interval == "Year":
				subscription.subscription_end_date = frappe.utils.add_months(subscription.start, d.qty*12)
			break
		subscription.save()
	else:
		frappe.throw(_('You cannot restart a Subscription that is not cancelled.'))

def update_invoices_long():
	enqueue("edu_custom.doctype_changes.update_invoices", queue='long', timeout=1500)

def update_invoices():
	data = frappe.db.sql("select name from `tabSales Invoice` where docstatus = 1")
	for d in data:
		generate_qr_for_print("Sales Invoice", d[0], "Invoice QR")