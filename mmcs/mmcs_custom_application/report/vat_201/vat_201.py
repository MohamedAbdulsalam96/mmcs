# Copyright (c) 2013, Bhavik Patel and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	if not filters: filters = {}
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data
	
	
def get_data(filters):
	if not (filters.get("company")):
		msgprint(_("Please select company"), raise_exception=1)
	if not (filters.get("month") and filters.get("year")):
		msgprint(_("Please select month and year"), raise_exception=1)
	
	standard_rate_1 = calc_standard_rate_1(filters.get("company"))
	standard_rate_1a = calc_standard_rate_1a(filters.get("company"))
	zero_rate_2 = calc_standard_rate_2(filters.get("company"))
	zero_rate_2a = calc_standard_rate_2a(filters.get("company"))
	
	doc =[standard_rate_1,standard_rate_1a,zero_rate_2,zero_rate_2a]
	return [doc]

def calc_standard_rate_1(company):
	return frappe.db.sql("select sum(amount) as `amount` from `tabSales Invoice Item` as siitem INNER JOIN `tabItem` as item on siitem.item_code=item.name INNER JOIN `tabSales Invoice` as invoice on invoice.name = siitem.parent  where siitem.docstatus=1 and invoice.company=%s ",company,as_dict=1)[0].amount

def calc_standard_rate_1a(company):
	return frappe.db.sql("select sum(amount) as `amount` from `tabSales Invoice Item` as siitem INNER JOIN `tabItem` as item on siitem.item_code=item.name INNER JOIN `tabSales Invoice` as invoice on invoice.name = siitem.parent  where siitem.docstatus=1 and invoice.company=%s ",company,as_dict=1)[0].amount

def calc_standard_rate_2(company):
	return frappe.db.sql("""select sum(amount) as `amount` from `tabSales Invoice Item` as siitem INNER JOIN `tabItem` as item on siitem.item_code=item.name INNER JOIN `tabSales Invoice` as invoice on invoice.name = siitem.parent INNER JOIN `tabSales Taxes and Charges` as tax on tax.parent = invoice.name   where siitem.docstatus=1 and invoice.company=%s and tax.account_head like %s """,(company,"%{0}%".format("Zero rated")),as_dict=1)[0].amount

def calc_standard_rate_2a(company):
	return frappe.db.sql("""select sum(amount) as `amount` from `tabSales Invoice Item` as siitem INNER JOIN `tabItem` as item on siitem.item_code=item.name INNER JOIN `tabSales Invoice` as invoice on invoice.name = siitem.parent INNER JOIN `tabSales Taxes and Charges` as tax on tax.parent = invoice.name   where siitem.docstatus=1 and invoice.company=%s and tax.account_head like %s """,(company,"%{0}%".format("Zero rated")),as_dict=1)[0].amount
	
	
def get_columns(filters):
	columns = [
		{
			"label": _("Standard Rate 1"),
			"fieldname": "standard_rate_1",
			"fieldtype": "Currency",
			"width": 180
		},
		{
			"label": _("Standard Rate 1A"),
			"fieldname": "standard_rate_1a",
			"fieldtype": "Currency",
			"width": 180
		},
		{
			"label": _("Zero Rate 2"),
			"fieldname": "zero_rate_2",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Zero Rate 2A"),
			"fieldname": "zero_rate_2a",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Excempt"),
			"fieldname": "excempt",
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"label": _("Vat on Standard Rate 4"),
			"fieldname": "vat_standard_rate_4",
			"fieldtype": "Currency",
			"width": 180
		},
		{
			"label": _("Vat on Standard Rate 4A"),
			"fieldname": "vat_standard_rate_4a",
			"fieldtype": "Currency",
			"width": 180
		},
		{
			"label": _("Second-hand Goods"),
			"fieldname": "second_hand",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Vat on Second-hand Goods"),
			"fieldname": "vat_second_hand",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Other Adjustment"),
			"fieldname": "other",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Total A"),
			"fieldname": "total_a",
			"fieldtype": "Currency",
			"width": 100
		}
	]
	return columns

