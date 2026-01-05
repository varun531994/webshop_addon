import frappe

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	user = frappe.session.user
	name = frappe.local.form_dict.get("name")

	if user == "Guest" or "Supplier" not in frappe.get_roles(user):
		frappe.throw("Not permitted", frappe.PermissionError)

	if not name:
		frappe.throw("Missing order")

	supplier = frappe.db.get_value(
		"Contact",
		{"user": user},
		"links.link_name"
	)

	doc = frappe.get_doc("Sales Order", name)

	if doc.custom_supplier != supplier:
		frappe.throw("Not permitted", frappe.PermissionError)

	context.doc = doc
	context.title = f"Order - {doc.name}"
	context.attachments = frappe.get_all(
		"File",
		filters={"attached_to_doctype": "Sales Order", "attached_to_name": doc.name},
		fields=["file_name", "file_url"]
	)
	context.parents = [{"name": "Home", "route": "/"},{"name": "Orders", "route": "/supplier-orders"}, ]
	return context