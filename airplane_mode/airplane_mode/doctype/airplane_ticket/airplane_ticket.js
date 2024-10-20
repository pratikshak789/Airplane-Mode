// Copyright (c) 2024, Pratiksha Khakse and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        // Add the "Actions" button
        frm.add_custom_button(__('Actions'), function() {
            // Show a dialog to assign the seat
            let d = new frappe.ui.Dialog({
                title: 'Select Seat',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                    }
                ],
                primary_action_label: 'Assign',
                primary_action(values) {
                    frm.set_value('seat', values.seat_number);
                    d.hide();
                }
            });

            // Show the dialog
            d.show();
        });
    }
});


