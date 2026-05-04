import frappe


@frappe.whitelist()
def get_dashboard_metrics():
    today = frappe.utils.today()
    orders_today = frappe.db.count("UV Order", {"creation": [">=", today]})
    revenue = frappe.db.sql(
        """select ifnull(sum(total_amount),0) from `tabUV Order` where date(creation)=curdate()"""
    )[0][0]
    low_stock = frappe.get_all("UV Product", filters={"stock_qty": ["<", 5]}, fields=["name", "sku", "stock_qty"], limit=20)

    return {
        "orders_today": orders_today,
        "revenue_today": revenue,
        "low_stock": low_stock,
    }
