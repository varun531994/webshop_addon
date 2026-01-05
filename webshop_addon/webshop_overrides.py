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

    # Only 10 Sales Orders can be assigned to a Supplier to manage Workload.
    MAX_ORDERS_PER_SUPPLIER = 10
    selected_supplier = None
    for s in suppliers:
        supplier_name = s.supplier
        so_count = frappe.db.count(
            "Sales Order",
            {
                "custom_supplier": supplier_name,
                "docstatus": ["!=", 2],  # optional: ignore cancelled
            },
        )
        if so_count < MAX_ORDERS_PER_SUPPLIER:
            selected_supplier = supplier_name
            break
    
    # If all suppliers for the given CUstomer location have more than 10 Orders assigned to them, then a Default Supplier is assigned to them as per workflow.
    if not selected_supplier:
        selected_supplier = "Default_Supplier"

    doc.custom_supplier = selected_supplier