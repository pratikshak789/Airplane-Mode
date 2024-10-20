# Copyright (c) 2024, Pratiksha Khakse and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import flt

def execute(filters=None):

    # Define columns for the report
    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airplane", "width": 150},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # Fetch airline data from the Airplane DocType
    airlines = frappe.get_all("Airplane", fields=["name as airline"])

    # Fetch revenue data for each airline using SQL query
    ticket_data = frappe.db.sql("""
        SELECT a.name AS airline, 
               SUM(at.total_amount) AS total_amount
        FROM `tabAirplane Ticket` at
        LEFT JOIN `tabAirplane` a ON at.flight = a.name
        GROUP BY a.name
    """, as_dict=True)

    # Fetch the total revenue (sum of all airline revenues)
    total_revenue_data = frappe.db.sql("""
        SELECT SUM(at.total_amount) AS total_revenue
        FROM `tabAirplane Ticket` at
        LEFT JOIN `tabAirplane` a ON at.flight = a.name
    """, as_dict=True)

    # Ensure the total revenue is fetched, else default to 0
    total_revenue = total_revenue_data[0].get('total_revenue', 0) if total_revenue_data else 0

    # Convert ticket data into a dictionary for easier lookup
    airline_revenue = {ticket['airline']: flt(ticket['total_amount']) for ticket in ticket_data}

    # Create the rows for each airline, even if there's no revenue
    data = []
    for airline in airlines:
        revenue = airline_revenue.get(airline['airline'], 0)
        data.append({
            "airline": airline['airline'],
            "revenue": revenue
        })

    # Add a summary section for total revenue
    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "datatype": "Currency",
            "indicator": "green"
        }
    ]

    # Create Donut Chart data
    chart = {
        "data": {
            "labels": [d['airline'] for d in data],
            "datasets": [{"values": [d['revenue'] for d in data]}],
        },
        "type": "donut",
    }

    # Add a total row at the bottom of the data
    data.append({
        "airline": "Total",
        "revenue": total_revenue,
        "is_bold": True 
    })

    # Return the columns, data, chart, and summary
    return columns, data, None, chart, summary
