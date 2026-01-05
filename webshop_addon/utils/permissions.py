import frappe

def sales_order_has_permission(doc, user):
    if user in ("Administrator",):
        return True

    roles = frappe.get_roles(user)

    # Customer logic remains unchanged
    if "Customer" in roles:
        return True

    if "Supplier" in roles:
        supplier = frappe.db.get_value(
            "Contact",
            {"user": user},
            "links.link_name"
        )
        return doc.custom_supplier == supplier

    return False