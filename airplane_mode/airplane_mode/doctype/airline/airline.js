// Copyright (c) 2024, Pratiksha Khakse and contributors
// For license information, please see license.txt


frappe.ui.form.on("Airline", {
    refresh(frm) {
        let website = frm.doc.website;

        if (website) {
            frm.add_web_link(website, "Visit Website");
        }
    }
});