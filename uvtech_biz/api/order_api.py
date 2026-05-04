import frappe


@frappe.whitelist()
def create_order_from_payload(payload):
    if isinstance(payload, str):
        payload = frappe.parse_json(payload)

    items = payload.get("items", [])
    order = frappe.get_doc(
        {
            "doctype": "UV Order",
            "order_id": payload.get("order_id"),
            "marketplace": payload.get("marketplace"),
            "order_date": payload.get("order_date") or frappe.utils.now_datetime(),
            "status": payload.get("status") or "Pending",
            "total_amount": payload.get("total_amount") or 0,
            "raw_data": payload,
            "items": [
                {"doctype": "UV Order Item", "sku": row.get("sku"), "qty": row.get("qty", 1), "rate": row.get("rate", 0)}
                for row in items
            ],
        }
    )
    order.insert(ignore_permissions=True)
    return {"name": order.name, "order_id": order.order_id}
