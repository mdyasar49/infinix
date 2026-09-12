# Odoo ERP Application Audit Report: CC Admin User (ccadmin)

**System URL:** https://app.canadiancrystalline.info | **Target Database:** CC_Live_Stage  
**Target User Profile:** CC Admin (ccadmin / UID: 11) | **Audit Scope:** 100% Exclusively Visible Applications, Process Compliance & Discuss Deep-Dive  
**Audit Date:** September 11, 2026 | **Prepared By:** Infogenx Senior ERP Technical Team  

---

## 1. CC Admin Authentication & Profile Details

| Parameter | Value |
| :--- | :--- |
| **Login Account** | `ccadmin` |
| **Login Password** | `CCAdm!n` |
| **Target Database** | `CC_Live_Stage` |
| **User ID (UID)** | 11 (Partner ID: 12) |
| **Assigned Role** | Sales & CRM Operations Manager (ccadmin) |
| **Scope of Audit** | Exclusively what is shown on screen to ccadmin (No hidden background modules) |

---

## 2. Inventory of Applications Actually Shown to CC Admin

When user **ccadmin** logs into the Odoo system, exactly **3 primary applications** and **4 global top-bar tools** are shown on screen:

| # | Shown Application / Tool | Navigation Location | Available Menus & Capabilities |
| :-: | :--- | :--- | :--- |
| 1 | **CRM** | Left Navigation Sidebar | Sales Pipeline, Leads, Scheduled Activities, Customers Directory, Reporting Analysis, Stage Configuration. |
| 2 | **Sales** | Left Navigation Sidebar | Quotations, Confirmed Sales Orders, Customers Master, Products Catalog, Sales Performance Reports. |
| 3 | **Settings** | Left Navigation Sidebar | Users & Companies (Users list and Company profile only). |
| 4 | **Discuss Messaging** | Top Right Navbar (Speech Bubble) | Direct staff chats, team channels, OdooBot notifications, and popover messaging panel. |
| 5 | **Activities Tracker** | Top Right Navbar (Clock Icon) | Lead follow-up reminders, calls, meetings, and email schedules. |
| 6 | **Company Switcher** | Top Right Navbar | Displays current active operating entity: `Canadian Crystaline` (Company ID: 1). |
| 7 | **User Profile Menu** | Top Right Navbar (CC Admin Avatar) | Profile Settings, Dark Mode Toggle, Documentation, Support, and Logout. |

### Screen 1: CC Admin Primary Sidebar Applications
- **Screen Name:** CC Admin Sidebar & Root Navigation
- **Screen URL:** [https://app.canadiancrystalline.info/odoo](https://app.canadiancrystalline.info/odoo)
- **Live Image:** ![CC Admin Sidebar Apps](https://files.catbox.moe/nlu6ne.png)
- **Verification Detail:** Verified that ccadmin only sees CRM, Sales, and Settings on the sidebar.

---

## 3. What Exists for ccadmin BESIDES CRM and Sales?

Apart from the core CRM and Sales modules, the following applications and tools are actually shown and active for **ccadmin**:

### A. Settings Module (Users & Companies Only)
The Settings icon appears on the left sidebar directly below Sales. Inside Settings, **ccadmin** is shown only the **Users & Companies** category:

| Shown Menu | Technical Model | Exact Capabilities Available to ccadmin |
| :--- | :--- | :--- |
| **Users** | `res.users` (Menu ID: 62) | View company team members (HODs, Sales Representatives, Lead User, Secretary), inspect assigned email addresses, and view active sales teams. |
| **Companies** | `res.company` (Menu ID: 58) | View the Canadian Crystaline company master record, including official address, GSTIN, and currency configuration. |

### Screen 2: CC Admin Settings Application (Users & Companies)
- **Screen Name:** Settings > Users & Companies
- **Screen URL:** [https://app.canadiancrystalline.info/odoo/settings](https://app.canadiancrystalline.info/odoo/settings)
- **Live Image:** ![CC Admin Settings](https://files.catbox.moe/nlpkwu.png)
- **Verification Detail:** Demonstrates that technical settings, developer mode switches, and server actions are completely restricted for ccadmin.

### B. Discuss Internal Messaging Widget
Shown as a speech bubble icon in the top navigation bar. It enables direct real-time communication between team members, sales reps, and department heads across Canadian Crystaline. (Detailed deep-dive in Section 8 below).

### C. Scheduled Activities Tracker
Shown as a clock icon in the top navbar. Aggregates all upcoming follow-up tasks, scheduled customer calls, and quotation deadlines into a single interactive popover.

---

## 4. Process Verification Audit: Lead Management Process.docx & Process flow.docx

A comprehensive technical audit was performed against the live Odoo database (`CC_Live_Stage`) to determine whether all requirements outlined in **Lead Management Process.docx** and **Process flow.docx** have been implemented:

### A. Fully Completed Requirements (Verified in Live System)

| # | Requirement Description | Reference Source | Live System Implementation Details | Status |
| :-: | :--- | :--- | :--- | :-: |
| 1 | All enquiries/leads created only by Lead User, Ms. Sandhiya | Lead Management P2 | User `sandhiya` (UID: 5) exists with dedicated login. Form contains Lead Source (`source_id`). | **Completed** |
| 2 | Source and Business Segment are separate fields | Process Flow P4 | `source_id` (Indiamart, TradeIndia, Website) and `business_segment_id` exist as separate independent dropdowns. | **Completed** |
| 3 | Automatic HOD assignment based on Business Segment | Lead Management P3 | HOD is automatically mapped and fetched based on `business_segment_id`. Button `action_auto_assign` is active. | **Completed** |
| 4 | HOD reviews enquiry, contacts customer, updates feedback | Lead Management P4 | HOD accounts (Murugan, Bushan, Ravi, Lakshmi, Sathish) have access to chatter feed to log notes and schedule activities. | **Completed** |
| 5 | Lead reassignment to Salesperson changes status to 'Allotted' | Lead Management P5 | Stage `Alloted` (Stage ID: 2, Sequence: 16) exists. Selecting a salesperson automatically transitions the stage. | **Completed** |
| 6 | Enquiry qualification statuses (Dropped, Repeated, Not in Scope) | Lead Management P6 | Stages configured: `Dropped` (ID 20), `Repeated` (ID 26), `Not Reachable` (ID 30), `Not In Scope Of Supply` (ID 31). | **Completed** |
| 7 | Dual visibility: HOD views salesperson's leads simultaneously | Lead Management P7 | Model `crm.lead.form.shared.users` (View ID: 2391) and record rules grant HOD continuous view of allotted leads. | **Completed** |
| 8 | Quotation request raised to Secretary | Lead Management P10 | Dedicated user `secretary` (UID: 17) exists. Stages `Quotation To Be Sent` and `Quotation Uploaded` handle workflow. | **Completed** |
| 9 | Secretary attaches quotation to lead | Lead Management P11 | Custom tab `crm_quotation_attachment` (View ID: 2389) allows uploading, previewing, and downloading quote files (.pdf, .docx, .xlsx). | **Completed** |
| 10 | Quotation must be approved by HOD before reassigning to Sales | Lead Management P12 | Model `crm.lead.form.stage.approval` (View ID: 2515) provides `Approve` and `Reject` buttons for stages `Quotation Approval Request` and `Quotation Approved`. | **Completed** |
| 11 | Tag field replaced with Product selection | Process Flow P6 | View ID: 2389 replaces tag usage with `product_ids` and product lines (`product_line_ids`) for Bottled Water, Brewery, PET, RFC. | **Completed** |
| 12 | Project Finalized Commercial & Payment History Table | Lead Management P16 | Custom tabs `crm_product_lines` and `crm_payment_lines` implement Total Value, Tax, Advance Received, and Pending balance. | **Completed** |
| 13 | HOD login lands directly on HOD Dashboard | Process Flow P13 | Menu `HOD Dashboard` (Menu ID: 518) exists and is configured as the default action for HOD user profiles. | **Completed** |

### B. Pending / Partial Items Requiring Final Configuration

| # | Requirement Description | Reference Source | Current Live Observation | Action Required to 100% Complete |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Remove Probability section from Sandhiya's panel** | Process Flow P3 | The `probability` field is still visible on the standard CRM lead form (View ID: 595). | Add `invisible="1"` or inherit view to hide `probability` for user `sandhiya`. |
| 2 | **Restrict Sandhiya from setting leads to 'LOST'** | Process Flow P8 | The 'Lost' button is available on the form header for general CRM users. | Restrict the `action_set_lost` button to groups `group_crm_hod` and `group_sale_manager` only. |
| 3 | **Rename Won stage to 'Quote Requested'** | Lead Management P9 | The final won stage in database is named `Project Finalized` (ID 4, is_won=True). Stage `Quote Requested` is an intermediate stage. | Adjust stage sequence and rename/map intermediate status to `Quote Requested` before `Project Finalized`. |
| 4 | **Ensure Territory is not auto-fetched with Source** | Lead Management P3 | The form still contains `territory_id` inside group in View 2372. | Verify server auto-assign logic so that `territory_id` is not mandatory or auto-populated if source only maps to segment. |

---

## 5. Exhaustive Branding Leak Audit: Every Location Where 'Odoo' & 'OdooBot' Appear

A rigorous scan of the **ccadmin** interface identified **6 specific locations** where unbranded Odoo labels are exposed:

| # | Component / Location | Exact Text / Code Encountered | Technical Impact on ccadmin | Remediation Action |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Discuss Systray Popover**<br>(Top Right Widget) | - `Install Odoo` (with Install button)<br>- `OdooBot: Welcome to the #general channel` | Opening the Discuss widget immediately displays 'Install Odoo' and OdooBot welcome message. | Disable Odoo PWA install prompt in web client assets and rename general channel creator. |
| 2 | **Discuss Direct Chats**<br>(9 Active Channels) | `OdooBot` appears in 9 conversation titles:<br>1. System Bot Alert Thread (ID: 3)<br>2. OdooBot, Sandhiya (ID: 4)<br>3. HOD Murugan, OdooBot (ID: 5)<br>4. OdooBot, Ramesh (ID: 6)<br>5. OdooBot, Secretary (ID: 7)<br>6. Nayana, OdooBot (ID: 8 & 9)<br>7. Mani, OdooBot (ID: 10)<br>8. HOD Ravi, OdooBot (ID: 11) | Direct chats list exposes OdooBot robot assistant to staff members. | Rename partner record #2 from `OdooBot` to `CC AI Assistant` or `System Bot`. |
| 3 | **User Profile -> Support Link**<br>(Top Right Dropdown) | `https://www.odoo.com/buy`<br>(Parameter: `base.web_support_url`) | Clicking Support opens official Odoo purchase page instead of company helpdesk. | Change `base.web_support_url` to internal support portal: `https://support.canadiancrystalline.com`. |
| 4 | **User Profile -> Documentation**<br>(Top Right Dropdown) | Redirects to official Odoo online user manuals (`odoo.com`). | Exposes underlying software framework to end users. | Point to internal Canadian Crystaline Standard Operating Procedures (SOP). |
| 5 | **Notification Accent Color**<br>(ir.config_parameter) | `email_secondary_color: '#875A7B'` | Official Odoo corporate purple color code used in automated notifications. | Update parameter to Canadian Crystaline navy blue (`#1a365d`) or orange (`#f2711c`). |
| 6 | **Automated Email Templates**<br>(12 mail.template records) | 12 templates contain raw Odoo text:<br>- *'invites you to connect to Odoo'*<br>- *'on your Odoo account'*<br>- *'Powered by Odoo'* (Email footers) | Automated invitation and reset emails display Odoo branding to clients and employees. | Execute bulk template text update to replace 'Odoo' with 'Canadian Crystaline'. |

---

## 6. Detailed Breakdown of Shown CRM Module for ccadmin

The CRM module interface shown to **ccadmin** provides complete operational control over sales leads and inquiries:

| Screen Name | Exact Navigation URL | Features Shown on Screen | Audit Observation |
| :--- | :--- | :--- | :--- |
| **CRM Pipeline** | `https://app.canadiancrystalline.info/odoo/crm` | Kanban board columns (New, Qualified, Proposition, Won), Opportunity cards, Deal revenue totals. | Cards render cleanly with drag-and-drop capability. Buttons use slate grey styling (#99a4ae). |
| **Opportunity Detail View** | `https://app.canadiancrystalline.info/odoo/crm/{id}` | Expected Revenue, Customer details, Probability %, Internal chatter feed, Schedule Activity button. | Quotation button directly connects lead to Sales module. |
| **Customers Directory** | `https://app.canadiancrystalline.info/odoo/res.partner` | Grid of customer profile cards with phone numbers, emails, and active orders count. | Clean presentation with full search and filtering capabilities. |
| **CRM Reporting** | `https://app.canadiancrystalline.info/odoo/crm.lead.report` | Pipeline analysis, conversion bar charts, and performance trend graphs. | Interactive charts render cleanly for sales tracking. |

### Screen 3: CC Admin CRM Pipeline Kanban View
- **Screen Name:** CRM > Sales Pipeline
- **Screen URL:** [https://app.canadiancrystalline.info/odoo/crm](https://app.canadiancrystalline.info/odoo/crm)
- **Live Image:** ![CRM Pipeline View](https://files.catbox.moe/jbcb02.png)
- **Verification Detail:** Displays the complete visual pipeline stages configured for Canadian Crystaline opportunities.

### Screen 4: CC Admin CRM Daily Sales Activity Dashboard
- **Screen Name:** CRM > Daily Sales Activity
- **Screen URL:** [https://app.canadiancrystalline.info/odoo/crm/daily_sales](https://app.canadiancrystalline.info/odoo/crm/daily_sales)
- **Live Image:** ![CRM Daily Sales](https://files.catbox.moe/s6lmtr.png)
- **Verification Detail:** Shows team activity tracking, customer follow-up metrics, and deal progression logs.

---

## 7. Detailed Breakdown of Shown Sales Module for ccadmin

The Sales module interface shown to **ccadmin** handles commercial pricing, quotation generation, and order confirmations:

| Screen Name | Exact Navigation URL | Features Shown on Screen | Audit Observation |
| :--- | :--- | :--- | :--- |
| **Quotations List** | `https://app.canadiancrystalline.info/odoo/sales/orders?view_type=list` | Table of draft quotations (e.g. S00012), Customer names, Salespersons, Quotation totals, Status badges. | Table renders cleanly with sortable columns and search filters. |
| **Sales Orders List** | `https://app.canadiancrystalline.info/odoo/sales/orders?view_type=list&sale_order=confirmed` | Confirmed customer purchase orders with invoicing status indicators. | Status accurately tracks commercial conversion from CRM pipeline. |
| **Quotation Form View** | `https://app.canadiancrystalline.info/odoo/sales/orders/{id}` | Product line items, Quantity, Unit price, Taxes, Total amount, Send by Email, Confirm Order buttons. | Clean status flow: Quotation -> Quotation Sent -> Sales Order. |
| **Products Catalog** | `https://app.canadiancrystalline.info/odoo/sales/products` | Equipment and item master cards, sales prices, cost prices, internal references. | Catalog items and pricing details display properly. |

### Screen 5: CC Admin Sales Quotations Management Table
- **Screen Name:** Sales > Quotations
- **Screen URL:** [https://app.canadiancrystalline.info/odoo/sales/orders?view_type=list](https://app.canadiancrystalline.info/odoo/sales/orders?view_type=list)
- **Live Image:** ![Sales Quotations](https://files.catbox.moe/c783y1.png)
- **Verification Detail:** Verified that ccadmin can view, filter, and review all sales proposals and quotations.

---

## 8. In-Depth Comprehensive Audit of the DISCUSS Messaging Screen

As specifically requested, a complete visual and technical investigation of the **Discuss Messaging System** was conducted. The Discuss widget is accessible to **ccadmin** directly from the top navigation bar (speech bubble icon):

### Screen 6: Live Odoo Discuss Messaging Widget & Popover Screen (Captured Under ccadmin Session)
- **Screen Name:** Discuss Systray Dropdown Panel
- **Screen URL:** [https://app.canadiancrystalline.info/odoo/action-mail.action_discuss](https://app.canadiancrystalline.info/odoo/action-mail.action_discuss) (Systray Speech Bubble)
- **Live Image:** ![Discuss Screen Popover](https://files.catbox.moe/pja32p.png)
- **Verification Detail:** Captured directly under user ccadmin session. Highlights unread notification badges, channel list, and the prominent 'Install Odoo' and 'OdooBot' branding leaks.

### A. Detailed Breakdown of the Discuss Popover Interface

When **ccadmin** clicks the speech bubble icon in the top right navbar, a rich popover window opens with the following key components:

| # | Component / Section | Visual / Functional Detail | Technical Model | Audit Finding |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Unread Badge Counter** | Displays a bright blue badge with unread message count (e.g., `2`) on top of the speech bubble icon. | `mail.notification` | Alerts ccadmin immediately to incoming direct messages or channel announcements. |
| 2 | **Navigation Tabs** | Three distinct filter tabs across the top: **Notifications**, **Chats**, and **Channels**. | Web Client Systray Component | Allows seamless switching between system alerts, private 1-on-1 staff conversations, and public company channels. |
| 3 | **New Message Action** | A dedicated `New Message` button in the top right of the popover header. | `discuss.channel.create` | Allows ccadmin to initiate a direct conversation with any staff member (Sandhiya, Murugan, Ramesh, Secretary) instantly. |
| 4 | **'Install Odoo' Prompt** | Displays: *'Install Odoo - Come here often? Install the app for quick and easy access!'* with an 'Install' button and close 'x'. | Web App PWA Service Worker | **CRITICAL BRANDING LEAK:** Explicitly prompts Canadian Crystaline staff to install Odoo software. |
| 5 | **'Turn on Notifications' Card** | Displays: *'Turn on notifications - Stay tuned! Enable push notifications to never miss a message.'* with an 'Enable' button. | HTML5 Web Notification API | Allows push notifications for urgent lead updates and quotation approvals. |
| 6 | **General Channel (#general)** | Displays: *'OdooBot: Welcome to the #general channel. This channel is accessible to all users to easily share company information.'* | `discuss.channel` (ID: 1) | **BRANDING LEAK:** First channel message visibly introduces 'OdooBot' to all employees. |

### B. Full Discuss Channels & Direct Chat Directory

In the live database, the Discuss system currently hosts **11 active communication channels** accessible to the administration team:

| Channel ID | Channel Name / Participants | Channel Type | Purpose & Workflow Role |
| :---: | :--- | :--- | :--- |
| 1 | **#general** | Public Company Channel | Company-wide announcements and general notifications. |
| 3 | **System Bot Alert Thread** | Direct Chat | Automated system notification channel. |
| 4 | **OdooBot, Sandhiya** | Direct Chat | Lead creator notification channel. |
| 5 | **HOD Murugan, OdooBot** | Direct Chat | Department Head review and lead allocation alerts. |
| 6 | **OdooBot, Ramesh** | Direct Chat | Sales representative quote request channel. |
| 7 | **OdooBot, Secretary** | Direct Chat | Quotation preparation and attachment alert thread. |
| 8 & 9 | **Nayana, OdooBot** | Direct Chat | Staff account notification threads. |
| 10 | **Mani, OdooBot** | Direct Chat | Staff account notification thread. |
| 11 | **HOD Ravi, OdooBot** | Direct Chat | Water division HOD alert thread. |

### C. Full-Screen Discuss Workspace (`/odoo/action-mail.action_discuss`)
When **ccadmin** opens the full-screen Discuss application, the left sidebar provides dedicated sections for **Inbox**, **Starred**, **History**, **Channels**, and **Direct Messages**. It includes full rich-text typing, file attachment uploads (PDFs, images, spreadsheets), voice memo support, and live user presence indicators (green online dot).

---

## 9. Color Palette & UI Styling Shown to ccadmin

| UI Element | Hex Code / Color | Screen Location | Audit Observation |
| :--- | :--- | :--- | :--- |
| **Primary Accent** | `#99a4ae` (Slate Grey) | Top navbar & active tabs | Clean appearance, but muted. Navy blue (`#1a365d`) would provide higher contrast. |
| **Header Background** | `#2c2f32` (Dark Charcoal) | Top bar container | Provides strong contrast against text and icons. |
| **Secondary Action** | `#665383` (Muted Purple) | Secondary buttons | Remnant of default Odoo button styling. Should be customized to corporate palette. |
| **Sidebar Void** | `#ffffff` (Blank Space) | Left sidebar below Settings | Displays empty vertical space of approx. 700px since only 3 apps are shown. |

---

## 10. Standard Business Process Flow for ccadmin

1. **Sign In:** Navigate to `https://app.canadiancrystalline.info` and log in with `ccadmin` / `CCAdm!n`.
2. **Pipeline Check:** Open **CRM** from the sidebar to inspect new opportunities on the Kanban board.
3. **Lead Qualification:** Click on an opportunity to review customer requirements and estimated contract value.
4. **Schedule Next Action:** Use the activity scheduler in the chatter panel to set a follow-up call or discovery meeting.
5. **Create Quotation:** Click **New Quotation** from the opportunity to generate a commercial proposal in **Sales**.
6. **Add Equipment & Pricing:** Add water treatment equipment lines, configure unit pricing, and verify tax amounts.
7. **Send Proposal:** Click **Send by Email** to deliver the quotation directly to the prospective client.
8. **Confirm Order:** Once accepted, click **Confirm** to lock the quote into an active Sales Order.
9. **Internal Messaging:** Use **Discuss** to coordinate with HODs, Sales Reps, and Secretary regarding quotation approvals.
10. **Staff Oversight:** Check **Settings -> Users & Companies -> Users** to ensure team assignments and contact information remain accurate.

---
*Report Compiled for Canadian Crystaline Water India Limited | Generated by Infogenx Senior Technical Audit Team*
