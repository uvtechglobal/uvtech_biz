import frappe
from frappe import _


def _validate_order_payload(payload):
    if not payload.get("order_id"):
        frappe.throw(_("order_id is required"))
    if not payload.get("marketplace"):
        frappe.throw(_("marketplace is required"))


def _is_internal_user():
    return frappe.session.user and frappe.session.user != "Guest"


@frappe.whitelist()
def create_order_from_payload(payload):
    if isinstance(payload, str):
        payload = frappe.parse_json(payload)

    if not _is_internal_user():
        frappe.throw(_("Authentication required"))

    _validate_order_payload(payload)

    existing = frappe.db.get_value("UV Order", {"order_id": payload.get("order_id")})
    if existing:
        return {"name": existing, "order_id": payload.get("order_id"), "status": "exists"}

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
                if row.get("sku")
            ],
        }
    )
    order.insert()
    return {"name": order.name, "order_id": order.order_id, "status": "created"}
