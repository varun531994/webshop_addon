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
        """, customer_pincode, as_dict=1
        )
    
    print(suppliers)
    MAX_ORDERS_PER_SUPPLIER = 10
    selected_supplier = None

    for s in suppliers:
        supplier_name = s.supplier
        print(supplier_name)
        so_count = frappe.db.count(
            "Sales Order",
            {
                "custom_supplier": supplier_name,
                "docstatus": ["!=", 2],  # optional: ignore cancelled
            },
        )
        print(so_count)
        if so_count < MAX_ORDERS_PER_SUPPLIER:
            selected_supplier = supplier_name
            break

    doc.custom_supplier = selected_supplier