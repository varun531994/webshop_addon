// frappe.ui.form.on('Delivery Note', {
//     refresh(frm) {
//         //if (frappe.user.has_role('Supplier') && frm.doc.supplier == frappe.defaults.get_user_default("Supplier") && frm.doc.delivered_by_customer && !frm.doc.payment_entry) {
//         if (frm.doc.supplier && !frm.doc.dispatched) {   
//             frm.add_custom_button(__('Payment Done'), function() {
//                 frappe.call({
//                     method: 'custom_app.overrides.mark_payment_done',
//                     args: { delivery_note: frm.doc.name },
//                     callback: (r) => {
//                         if (!r.exc) {
//                             frappe.msgprint(__('Sales Invoice {0} created', [r.message]));
//                             frm.reload_doc();
//                         }
//                     }
//                 });
//             });
//         }
//     }
// });
