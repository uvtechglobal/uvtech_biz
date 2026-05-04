import frappe


def set_default_workspace():
    user = frappe.session.user
    if not user or user == "Guest":
        return
    if frappe.db.get_value("User", user, "desk_theme") is None:
        return
    frappe.db.set_value("User", user, "desk_theme", "Light", update_modified=False)
    frappe.db.set_value("User", user, "home_page", "/app/uvtech-biz", update_modified=False)
