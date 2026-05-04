import frappe
from uvtech_biz.api.order_api import create_order_from_payload
from uvtech_biz.marketplace.shopify.api import fetch_orders


def sync_orders():
    orders = fetch_orders()
    for payload in orders:
        try:
            result = create_order_from_payload(payload)
            log_status("Shopify", "Success", f"{result.get('status')}: {payload.get('order_id')}")
        except Exception as exc:
            log_status("Shopify", "Failed", str(exc))
            frappe.log_error(frappe.get_traceback(), "UV Order Sync Failed")


def log_status(platform, status, message):
    frappe.get_doc({
        "doctype": "UV Sync Log",
        "platform": platform,
        "status": status,
        "message": message,
    }).insert(ignore_permissions=True)
