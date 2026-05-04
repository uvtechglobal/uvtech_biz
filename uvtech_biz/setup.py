import frappe

DOCTYPE_LIST = [
    "uv_company_registration",
    "uv_subscription",
    "uv_product",
    "uv_customer",
    "uv_order_item",
    "uv_order",
    "uv_marketplace_account",
    "uv_stock_ledger",
    "uv_sync_log",
]


def ensure_setup():
    ensure_module_def()
    reload_uv_doctypes()
    reload_workspace()


def ensure_module_def():
    if frappe.db.exists("Module Def", "Uvtech Biz"):
        return
    frappe.get_doc(
        {
            "doctype": "Module Def",
            "module_name": "Uvtech Biz",
            "app_name": "uvtech_biz",
        }
    ).insert(ignore_permissions=True)


def reload_uv_doctypes():
    for dt in DOCTYPE_LIST:
        frappe.reload_doc("uvtech_biz", "doctype", dt, force=True)


def reload_workspace():
    frappe.reload_doc("uvtech_biz", "workspace", "uvtech_biz", force=True)
