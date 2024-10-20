# Copyright (c) 2024, Pratiksha Khakse and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):

    
    def on_submit(self):
        self.status = "Completed"