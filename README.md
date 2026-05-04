# UVTech Biz (Frappe v16)

UVTech Biz is a lightweight, production-ready SaaS app for **multi-marketplace order and inventory management** on the Frappe Framework.

This MVP is designed for retail sellers who need one clean place to:
- collect orders from multiple channels,
- keep stock updated,
- and monitor daily operations with minimal UI overhead.

---

## Core MVP Capabilities

### 1) Master Site (Super Admin)
- Company onboarding via **UV Company Registration**.
- Subscription tracking via **UV Subscription**.
- Approve/reject registration through API workflow.
- Approval API includes placeholders for:
  - site creation,
  - app installation,
  - admin user setup.

### 2) Client Site (Per Company)
- **Products** with SKU, price, and stock.
- **Customers** auto-created from incoming order payloads.
- **Orders + Order Items** in a unified structure.
- **Marketplace Accounts** for channel credentials and sync controls.
- **Stock Ledger** for inventory movement history.
- **Sync Logs** for operational traceability.

### 3) Marketplace Ingestion
- Shared abstraction: `create_order_from_payload(payload)`.
- CSV import engine for quick onboarding and backfills.
- Shopify adapter stub to plug in real API calls.

### 4) Inventory & Controls
- Stock deduction automatically on order insert.
- Stock ledger entry per order item movement.
- Daily subscription order limit check before order creation.

### 5) Scheduler & Dashboard
- Scheduler job every 15 minutes for marketplace sync.
- Dashboard metrics API:
  - orders today,
  - revenue today,
  - low stock products.

---

## Project Structure

```text
uvtech_biz/
├── api/
├── dashboard/
├── marketplace/
│   ├── shopify/
│   ├── amazon/csv/
│   ├── flipkart/csv/
│   └── meesho/csv/
├── scheduler/
├── hooks.py
└── uvtech_biz/doctype/
```

---

## Installation (Frappe Bench)

> Assumes Python, Node.js, Redis, MariaDB, and wkhtmltopdf prerequisites are already installed for Frappe v16.

1. Create a bench (if you don't already have one):
```bash
bench init frappe-bench --frappe-branch version-16
cd frappe-bench
```

2. Get this app into `apps/`:
```bash
bench get-app uvtech_biz <YOUR_REPO_URL>
```

3. Create a site:
```bash
bench new-site biz.uvtecherp.in
```

4. Install the app on the site:
```bash
bench --site biz.uvtecherp.in install-app uvtech_biz
```

5. Run migrations:
```bash
bench --site biz.uvtecherp.in migrate
```

6. Start development server:
```bash
bench start
```

---

## Production Notes (Frappe Cloud)

- Use **separate sites per company** for clean multi-tenant isolation.
- Keep one dedicated **master site** for onboarding + subscription control.
- Store marketplace credentials securely in DocTypes with appropriate role permissions.
- Replace Shopify stub with real OAuth/private app flow before go-live.

---

## API Endpoints (Whitelisted Functions)

- `uvtech_biz.api.master_api.approve_company`
- `uvtech_biz.api.master_api.reject_company`
- `uvtech_biz.api.order_api.create_order_from_payload`
- `uvtech_biz.api.csv_import.import_orders_from_csv`
- `uvtech_biz.dashboard.metrics.get_dashboard_metrics`

---

## Roles

- **Company Admin**: full access.
- **Staff**: operational access for orders and inventory.

---

## License

MIT
