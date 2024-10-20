# Copyright (c) 2024, Pratiksha Khakse and contributors
# For license information, please see license.txt


import random
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_addons() 

		total_price = 0
		for item in self.add_ons:
			total_price += item.amount

		self.total_amount = self.flight_price + total_price

	def remove_duplicate_addons(self):
		seen_add_ons = set()
		unique_add_ons = []
		
		for add_on in self.add_ons:
			if add_on.add_on_type not in seen_add_ons:
				unique_add_ons.append(add_on)
				seen_add_ons.add(add_on.add_on_type)
		self.add_ons = unique_add_ons

	def before_insert(self):
		seat_number = random.randint(1, 100)  
		seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])  
		self.seat = f"{seat_number}{seat_letter}"
		
	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("You cannot submit a ticket that is not marked as 'Boarded'.", frappe.ValidationError)

	def validate(self):
		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity
		
		tickets_count = frappe.db.count('Airplane Ticket', filters={'flight': self.flight})
		
		if tickets_count >= capacity:
			frappe.throw(f"This flight is full. Cannot book more than {capacity} tickets for this flight.")