import frappe


@frappe.whitelist()
def approve_company(registration_id):
    reg = frappe.get_doc("UV Company Registration", registration_id)
    reg.status = "Approved"
    reg.save(ignore_permissions=True)

    site_name = f"{frappe.scrub(reg.company_name)}.biz.uvtecherp.in"
    return {
        "status": "approved",
        "site": site_name,
        "actions": [
            "create_site_placeholder",
            "install_uvtech_biz_app",
            "create_admin_user",
        ],
    }


@frappe.whitelist()
def reject_company(registration_id):
    reg = frappe.get_doc("UV Company Registration", registration_id)
    reg.status = "Rejected"
    reg.save(ignore_permissions=True)
    return {"status": "rejected", "registration": reg.name}
