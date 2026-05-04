import frappe
from frappe import _
from frappe.model.document import Document


class UvOrder(Document):
    def before_insert(self):
        check_order_limit()
        self._ensure_customer()

    def after_insert(self):
        update_inventory_for_order(self)

    def _ensure_customer(self):
        if self.customer:
            return

        data = self.raw_data if isinstance(self.raw_data, dict) else {}
        email = data.get("customer_email")
        customer_name = data.get("customer_name") or f"Customer-{self.order_id}"

        existing = frappe.db.get_value("UV Customer", {"email": email}) if email else None
        if existing:
            self.customer = existing
            return

        customer = frappe.get_doc({
            "doctype": "UV Customer",
            "customer_name": customer_name,
            "email": email,
            "phone": data.get("customer_phone"),
        })
        customer.insert(ignore_permissions=True)
        self.customer = customer.name


def check_order_limit():
    subscription = frappe.get_all(
        "UV Subscription",
        filters={"status": "Active"},
        fields=["name", "order_limit"],
        order_by="modified desc",
        limit=1,
    )
    if not subscription:
        return

    order_limit = subscription[0].order_limit or 0
    if order_limit <= 0:
        return

    order_count = frappe.db.count("UV Order", filters={"creation": ["between", [frappe.utils.today(), frappe.utils.now()]]})
    if order_count >= order_limit:
        frappe.throw(_("Daily order limit reached for current subscription."))


def update_inventory_for_order(order_doc):
    for item in order_doc.get("items", []):
        product_name = frappe.db.get_value("UV Product", {"sku": item.sku})
        if not product_name:
            continue

        current_stock = frappe.db.get_value("UV Product", product_name, "stock_qty") or 0
        new_stock = float(current_stock) - float(item.qty)
        frappe.db.set_value("UV Product", product_name, "stock_qty", new_stock, update_modified=False)

        ledger = frappe.get_doc({
            "doctype": "UV Stock Ledger",
            "product": product_name,
            "qty_change": -float(item.qty),
            "source": "Order",
            "reference": order_doc.name,
        })
        ledger.insert(ignore_permissions=True)
