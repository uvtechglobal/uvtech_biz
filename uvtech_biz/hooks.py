app_name = "uvtech_biz"
app_title = "UVTech Biz"
app_publisher = "UVTech"
app_description = "Multi-marketplace order and inventory SaaS"
app_email = "support@uvtecherp.in"
app_license = "MIT"

scheduler_events = {
    "cron": {
        "*/15 * * * *": [
            "uvtech_biz.scheduler.sync_jobs.sync_orders"
        ]
    }
}

fixtures = []


after_migrate = [
    "uvtech_biz.setup.ensure_setup"
]

after_install = "uvtech_biz.setup.ensure_setup"
<<<<<<< codex/build-uvtech_biz-saas-app-on-frappe-x6v51w


before_migrate = "uvtech_biz.setup.ensure_setup"


on_session_creation = "uvtech_biz.branding.set_default_workspace"
=======
>>>>>>> main
