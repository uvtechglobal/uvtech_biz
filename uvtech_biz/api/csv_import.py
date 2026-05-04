import csv
import io
import frappe
from uvtech_biz.api.order_api import create_order_from_payload


@frappe.whitelist()
def import_orders_from_csv(content, marketplace="CSV"):
    if not content:
        frappe.throw("CSV content is required")

    if isinstance(content, str):
        decoded = content
    else:
        decoded = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(decoded))
    grouped = {}

    for row in reader:
        order_id = row.get("order_id")
        if not order_id:
            continue
        grouped.setdefault(order_id, []).append(row)

    created = []
    for order_id, rows in grouped.items():
        payload = {
            "order_id": order_id,
            "marketplace": marketplace,
            "items": [
                {"sku": r.get("sku"), "qty": float(r.get("qty") or 1), "rate": float(r.get("rate") or 0)} for r in rows
            ],
        }
        created.append(create_order_from_payload(payload))

    return {"created": created, "count": len(created)}
