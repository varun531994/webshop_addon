frappe.ready(() => {
    $('.dispatch-btn').click(function () {
        var sales_order = $(this).attr('data-name') || $(this).data('name');
        dispatch_order(sales_order)
    })

    function dispatch_order (sales_order) {
        frappe.call({
            method:"webshop_addon.templates.pages.order.create_delivery_note",
            args: {
                order: sales_order
            },
            freeze:true,
            callback: function(r) {
                if(!r.exc) {
                    $('.dispatch-btn').hide();
                    frappe.msgprint({
                        title: 'Dispatched!',
                        indicator: 'green',
                        message: `DN <b>${r.message.dn_name}</b> submitted`
                    });
                }

            }
        })

    }

    $('.mark-delivered-btn').click(function (){
        var sales_order = $(this).attr('data-name') || $(this).data('name');
        ack_delivery(sales_order)
    })

    function ack_delivery (sales_order) {
        frappe.call({
            method:"webshop_addon.templates.pages.order.create_payment_and_bill",
            args: {
                order: sales_order,
            },
            freeze:true,
            callback: function(r) {
                if(!r.exc) {
                   $('.mark-delivered-btn').hide();
                    frappe.msgprint({
                        title: 'Sales Invoice Generated!!',
                        indicator: 'green',
                        message: `A Sales Invoice: <b>${r.message.si_name}</b> has been generated for the Order: ${r.message.so_name}. Happy Shopping!!`
                    });
                }

            }
        })

    }
})