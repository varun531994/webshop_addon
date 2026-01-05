import frappe
from frappe import _

def assign_supplier_for_order(doc, method=None):
    
    shipping_address = doc.shipping_address_name

    customer_pincode = frappe.db.get_value('Address', shipping_address, 'pincode')

    suppliers = frappe.db.sql("""
            SELECT DISTINCT dl.link_name as supplier
            FROM `tabDynamic Link` dl
            INNER JOIN `tabAddress` a ON dl.parent = a.name
            WHERE dl.link_doctype = 'Supplier'
            AND a.pincode = %s
            AND a.disabled = 0
            LIMIT 1
        """, customer_pincode, as_dict=1
        )

    doc.custom_supplier = suppliers[0].supplier if suppliers else None