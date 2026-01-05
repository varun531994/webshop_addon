# import frappe
# from frappe import _
# from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
# from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

# @frappe.whitelist()
# def dispatch_order(sales_order):
#     so = frappe.get_doc("Sales Order", sales_order)
#     if so.docstatus != 1 or so.status == "Closed":
#         frappe.throw("Sales Order must be submitted and open")
    
#     # Create Delivery Note
#     dn = make_delivery_note(so.name)
#     dn.supplier = so.supplier  # Custom field
#     dn.insert()
#     dn.submit()
    
#     # Update SO
#     so.db_set("dispatched", 1)
#     frappe.db.commit()
#     return dn.name

# @frappe.whitelist()
# def make_delivery_note(source_name):
#     from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
#     return make_delivery_note(source_name)

# @frappe.whitelist()
# def mark_delivered(delivery_note):
#     dn = frappe.get_doc("Delivery Note", delivery_note)
#     if dn.docstatus != 1:
#         frappe.throw("Delivery Note must be submitted")
    
#     dn.db_set("delivered_by_customer", 1)
    
#     # Auto create Payment Entry for COD (supplier receives payment)
#     pe = get_payment_entry(dt="Delivery Note", dn=dn.name, party=dn.customer)
#     pe.payment_type = "Receive"  # Customer pays supplier
#     pe.mode_of_payment = "Cash"  # COD
#     pe.insert()
#     pe.submit()
    
#     dn.db_set("payment_entry", pe.name)
#     frappe.db.commit()
#     return pe.name

# @frappe.whitelist()
# def mark_payment_done(delivery_note):
#     dn = frappe.get_doc("Delivery Note", delivery_note)
#     pe_name = dn.payment_entry
#     if not pe_name:
#         frappe.throw("No Payment Entry found")
    
#     # Create Sales Invoice from DN
#     si = make_sales_invoice(dn.name)
#     si.insert()
#     si.submit()
    
#     frappe.db.commit()
#     return si.name