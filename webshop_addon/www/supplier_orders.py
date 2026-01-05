import frappe

STATUS_COLORS = {
	"Draft": "gray",
	"To Deliver and Bill": "orange",
	"To Deliver": "orange",
	"To Bill": "orange",
	"Completed": "green",
	"Cancelled": "red",
	}

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	user = frappe.session.user

	if user == "Guest" or "Supplier" not in frappe.get_roles(user):
		frappe.throw("Not permitted", frappe.PermissionError)

	supplier = frappe.db.get_value(
		"Contact",
		{"user": user},
		"links.link_name"
	)

	if not supplier:
		context.orders = []
		return context

	orders = frappe.get_all(
		"Sales Order",
		filters={
			"custom_supplier": supplier,
			"docstatus": 1
		},
		fields=[
			"name",
			"transaction_date",
			"status",
			"grand_total",
			"currency"
		],
		order_by="transaction_date desc"
	)

	# Add indicator_color like webshop does

	for d in orders:
		d.indicator_color = STATUS_COLORS.get(d.status, "blue")

	context.orders = orders
	return context