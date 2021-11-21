from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe
from datetime import date, datetime
import json
from frappe import utils
import datetime

no_cache = 1

@frappe.whitelist(allow_guest=True)
def get_attendance_data(stud_id=None):

	student_id = stud_id
	response = {}


	student = frappe.db.get_value("Student", {"name": student_id}, "customer")
	if not student:
		response['message'] = 'invalid_id'
		return response

	response['student'] = student

	subscription_status = frappe.db.get_value("Subscription", {"customer": student}, "status")
		
	if not subscription_status or subscription_status != 'Active':
		response['message'] = 'resubscribe'
		return response

	
	attendance_status = frappe.db.get_value("Student Attendance", {"student": student_id, "date": datetime.date.today()}, "status")

	if attendance_status:
		response['attendance'] = attendance_status
		return response

	return response


@frappe.whitelist(allow_guest=True)
def mark_attendance(student_id=None, mark_attendance=None):
	response = {}

	if mark_attendance and student_id:
		student_group = frappe.db.get_value("Student Group Student", {"student": student_id}, "parent")
		# if not student_group:
		# 	response['message'] = 'set_student_group'
		# 	return response

		new_attendance_doc = frappe.new_doc("Student Attendance")
		new_attendance_doc.update({"student": student_id, "date": datetime.date.today(), "student_group":student_group , "status": "Present"})
		new_attendance_doc.insert(ignore_permissions=True)
		frappe.db.commit()

		attendance_status = frappe.db.get_value("Student Attendance", {"student": student_id, "date": datetime.date.today()}, "status")
		response['attendance'] = new_attendance_doc.status
		return response
	return response
