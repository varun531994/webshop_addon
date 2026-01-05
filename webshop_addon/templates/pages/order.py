
import frappe
from frappe import _

from webshop.templates.pages.order import get_context as _get_context

def get_context(context):
    _get_context(context)

@frappe.whitelist()
def create_delivery_note(order):
    from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note

    dn = make_delivery_note(order)
    dn.flags.ignore_permissions = True
    dn.insert()
    dn.submit()

    return {
        "dn_name": dn.name
    }

@frappe.whitelist()
def create_payment_and_bill(order):
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
    from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
    from webshop.webshop.shopping_cart.cart import get_party

    #make payment entry
    party = get_party()
    
    payment_entry = get_payment_entry(
            dt='Sales Order', 
            dn=order, 
            payment_type='Receive', 
            party_type='Customer'
    )

    payment_entry.update({
        "party": party.name,
        "mode_of_payment": "Cash"
    })
    payment_entry.flags.ignore_permissions = True
    payment_entry.insert()
    payment_entry.submit()

    #make sales invoice
    sales_invoice = make_sales_invoice(order, ignore_permissions = True)
    sales_invoice.allocate_advances_automatically = 1 #as we are collecting payment against SO it will get consider as advance
    sales_invoice.set_advances()
    sales_invoice.insert()
    sales_invoice.submit()

    return {
        "pe_name": payment_entry.name,
        "si_name": sales_invoice.name,
        "so_name": order
    }
    