// frappe.ui.form.on('Sales Order', {
//     refresh(frm) {
//         //if (frappe.user.has_role('Supplier') && frm.doc.supplier == frappe.defaults.get_user_default("Supplier") && !frm.doc.dispatched) {
//         if (frm.doc.supplier && !frm.doc.dispatched) {     
//             frm.add_custom_button(__('Dispatch Order'), function() {
//                 frappe.call({
//                     method: 'custom_app.overrides.dispatch_order',
//                     args: { sales_order: frm.doc.name },
//                     callback: (r) => {
//                         if (!r.exc) {
//                             frappe.msgprint(__('Delivery Note {0} created', [r.message]));
//                             frm.reload_doc();
//                         }
//                     }
//                 });
//             });
//         }
//     }
// });
