import frappe


def fetch_orders(account_name=None):
    filters = {"platform": "Shopify", "sync_enabled": 1}
    if account_name:
        filters["name"] = account_name

    accounts = frappe.get_all("UV Marketplace Account", filters=filters, fields=["name", "api_key", "api_secret", "seller_id"])

    all_orders = []
    for account in accounts:
        # Placeholder for actual Shopify API integration
        sample = {
            "order_id": f"SHOP-{frappe.generate_hash(length=8)}",
            "marketplace": "Shopify",
            "status": "Pending",
            "total_amount": 0,
            "items": [],
            "source_account": account.name,
        }
        all_orders.append(sample)

    return all_orders
