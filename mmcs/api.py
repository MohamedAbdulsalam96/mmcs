from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint,throw, _


@frappe.whitelist()
def make_rfq(source_name, target_doc=None):
	return frappe.new_doc("Request for Quotation")
	
	
@frappe.whitelist()
def test():
	return today()

