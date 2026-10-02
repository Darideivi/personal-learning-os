# Graph Report - Desktop  (2026-10-02)

## Corpus Check
- 114 files · ~404,754 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 780 nodes · 1723 edges · 47 communities (30 shown, 17 thin omitted)
- Extraction: 93% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 111 edges (avg confidence: 0.88)
- Token cost: 292,321 input · 0 output

## Community Hubs (Navigation)
- Website Layout & Pages
- Contracting OS Vision & Opportunity Sourcing
- Vendored AdminLTE JS (noise)
- COMMBUYS Scraper Service
- Geo Radius Filter (Lawrence MA)
- Leads Table, RLS & Leads Module
- Supabase Client & Login Guard
- Homelab n8n, Cloudflare & Google
- Walkthrough Form → submitLead
- Ecosystem Architecture & Deploy
- Flask App Factory & Config
- Vendored AdminLTE Accessibility (noise)
- Website TypeScript Config
- Logo Preparation Script
- Opportunities List & Past Searches
- Website Lint & Package Meta
- Security Review & Dependencies
- Website Brand & Content Brief
- Dashboard & Company Profile
- Badge & Video Generation Scripts
- Spam Protection: Honeypot + Turnstile
- Website Dev Dependencies
- Website npm Scripts
- CSRF-Protected App Forms
- Vendored AdminLTE Theme (noise)
- Opportunities Table Migration
- Website Runtime Dependencies
- Login & Base Layout
- COMMBUYS Bids Export & Attachments
- Phase 1 Base Schema
- Opportunities Alignment Migration
- Screenshot QA Script
- Opportunity Searches Migration
- Vercel Python Deploy Config
- Social Image Script
- Opportunity Sorting
- PostCSS Config
- Supabase MCP Config

## God Nodes (most connected - your core abstractions)
1. `get_supabase()` - 36 edges
2. `login_required()` - 29 edges
3. `Supabase leads table` - 27 edges
4. `GD Focus Ecosystem System Map` - 24 edges
5. `Container()` - 23 edges
6. `Icon()` - 23 edges
7. `f` - 21 edges
8. `Ve` - 21 edges
9. `Supabase` - 20 edges
10. `xe` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Supabase anon vs service role key` --conceptually_related_to--> `createServerSupabase()`  [AMBIGUOUS]
  GD_Focus_Solutions/learning/concepts-to-learn/README.md → Company_website/src/lib/supabase-server.ts
- `Lead Status Lifecycle (new to converted/closed)` --conceptually_related_to--> `update_lead()`  [INFERRED]
  GD-Focus-Ecosystem/README.md → GD_Focus_Solutions/app/leads/routes.py
- `import_past_due_sam.py tool` --semantically_similar_to--> `search_opportunities()`  [INFERRED] [semantically similar]
  GD_Focus_Solutions/tools/README.md → GD_Focus_Solutions/app/services/sam_gov_service.py
- `submitLead()` --conceptually_related_to--> `anon_insert_website_lead RLS Policy`  [INFERRED]
  Company_website/src/app/actions/submitLead.ts → GD-Focus-Ecosystem/plans/PHASE1_IMPLEMENTATION_PLAN.md
- `GD Focus Website Implementation Plan` --references--> `submitLead()`  [INFERRED]
  GD-Focus-Ecosystem/plans/WEBSITE_IMPLEMENTATION.md → Company_website/src/app/actions/submitLead.ts

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Website lead intake pipeline** — concept_website_gdfacility, concept_supabase_leads_table, gd_focus_solutions_ecosystem_integration_leads_module, concept_n8n, concept_gmail, gd_focus_solutions_migrations_0013_create_leads [EXTRACTED 1.00]
- **Login and session security hardening** — gd_focus_solutions_security_review_csrf_protection, gd_focus_solutions_security_review_session_cookie_flags, gd_focus_solutions_security_review_security_headers, gd_focus_solutions_security_review_login_rate_limiting, gd_focus_solutions_security_review_error_message_sanitization, gd_focus_solutions_security_review_auth_failure_logging, gd_focus_solutions_security_review_secret_key_hard_fail [EXTRACTED 1.00]
- **Opportunity sourcing with radius filter** — gd_focus_solutions_app_services_sam_gov_service_search_opportunities, gd_focus_solutions_app_services_commbuys_service_search_bids, gd_focus_solutions_session_handoff_geo_helpers, gd_focus_solutions_session_handoff_lawrence_radius_filter, gd_focus_solutions_session_handoff_opportunity_searches, gd_focus_solutions_project_opportunities_module [INFERRED 0.85]
- **Opportunity search, save and import flow** — gd_focus_solutions_app_templates_opportunities_import_search_form, gd_focus_solutions_app_templates_opportunities__results_table, gd_focus_solutions_app_templates_opportunities__results_table_import_select_form, gd_focus_solutions_app_templates_opportunities_searches, gd_focus_solutions_app_templates_opportunities_search_detail, gd_focus_solutions_app_templates_opportunities_search_detail_rerun_search_form [INFERRED 0.85]
- **Website lead triage flow** — gd_focus_solutions_app_templates_dashboard_index_new_website_leads_card, gd_focus_solutions_app_templates_leads_index, gd_focus_solutions_app_templates_leads_detail, gd_focus_solutions_app_templates_leads_detail_follow_up_form, concept_supabase_leads_table [INFERRED 0.85]
- **CSRF-protected POST forms** — gd_focus_solutions_app_templates_auth_login_login_form, gd_focus_solutions_app_templates_company_profile_profile_form, gd_focus_solutions_app_templates_documents_index_upload_form, gd_focus_solutions_app_templates_documents_index_delete_form, gd_focus_solutions_app_templates_leads_detail_follow_up_form, gd_focus_solutions_app_templates_opportunities__results_table_import_select_form, gd_focus_solutions_app_templates_opportunities_detail_refresh_form, gd_focus_solutions_app_templates_opportunities_detail_delete_form, gd_focus_solutions_app_templates_opportunities_detail_pipeline_status_form, gd_focus_solutions_app_templates_opportunities_import_search_form, gd_focus_solutions_app_templates_opportunities_search_detail_rerun_search_form, gd_focus_solutions_app_templates_opportunities_searches_delete_search_form [EXTRACTED 1.00]
- **Website lead capture: form -> Turnstile -> submitLead -> leads -> Command Center Leads view** — company_website_src_components_sections_walkthroughform_walkthroughform, company_website_src_components_ui_turnstile_turnstile, company_website_src_lib_turnstile_verifyturnstile, company_website_src_lib_lead_schema_leadschema, company_website_src_app_actions_submitlead_submitlead, company_website_src_lib_supabase_server_createserversupabase, concept_supabase_leads_table, gd_focus_ecosystem_plans_phase1_implementation_plan_anon_insert_website_lead_policy, gd_focus_solutions_app_leads_routes_list_leads, gd_focus_solutions_app_leads_routes_view_lead, gd_focus_solutions_app_leads_routes_update_lead, gd_focus_solutions_app_dashboard_routes_new_lead_count [EXTRACTED 1.00]
- **Lead notification: leads INSERT -> DB webhook -> n8n -> Gmail owner alert + customer confirmation** — concept_supabase_leads_table, concept_supabase_db_webhook, gd_focus_ecosystem_plans_phase1_implementation_plan_x_webhook_secret_header, gd_focus_ecosystem_homelab_n8n_homelab_handoff_n8n_webhooks_bypass_app, concept_n8n, concept_gmail, gd_focus_ecosystem_plans_phase1_implementation_plan_owner_new_lead_alert, gd_focus_ecosystem_plans_phase1_implementation_plan_customer_confirmation_email [EXTRACTED 1.00]
- **n8n homelab exposure stack (Docker, Tunnel, Access, OTP)** — concept_homelab, gd_focus_ecosystem_homelab_n8n_homelab_handoff_n8n_container, gd_focus_ecosystem_homelab_n8n_homelab_handoff_cloudflared_container, concept_cloudflare_tunnel, concept_cloudflare_access, gd_focus_ecosystem_homelab_n8n_homelab_handoff_n8n_editor_access_app, gd_focus_ecosystem_homelab_n8n_homelab_handoff_n8n_webhooks_bypass_app, gd_focus_ecosystem_homelab_n8n_homelab_handoff_email_otp_idp [EXTRACTED 1.00]

## Communities (47 total, 17 thin omitted)

### Community 0 - "Website Layout & Pages"
Cohesion: 0.07
Nodes (64): nextConfig, securityHeaders, allura, jsonLd, metadata, montserrat, publicSans, shareImage (+56 more)

### Community 1 - "Contracting OS Vision & Opportunity Sourcing"
Cohesion: 0.07
Nodes (41): COMMBUYS, SAM.gov, Opportunities Module (SAM.gov + COMMBUYS), USASpending API, phase1_schema migration, Opportunity search criteria form, CLAUDE.md (GD_Focus_Solutions), Database migrations (+33 more)

### Community 2 - "Vendored AdminLTE JS (noise)"
Cohesion: 0.06
Nodes (8): ce, f, ge, ne, p, pe(), Ue, xe

### Community 3 - "COMMBUYS Scraper Service"
Cohesion: 0.07
Nodes (20): _clean_contact_name(), _detail_fields(), _extract_amendments(), _extract_attachments(), _extract_item_descriptions(), _extract_requirements(), _extract_unspsc(), _fetch_detail() (+12 more)

### Community 4 - "Geo Radius Filter (Lawrence MA)"
Cohesion: 0.07
Nodes (17): distance_from_lawrence(), _geocode(), get_city_coordinates(), get_place_coordinates(), get_zip_coordinates(), is_cached(), state_distance(), state_may_be_in_radius() (+9 more)

### Community 5 - "Leads Table, RLS & Leads Module"
Cohesion: 0.10
Nodes (28): Row Level Security (RLS), Supabase leads table, Dashboard (New website leads card), Leads Module (Command Center), anon_insert_website_lead RLS Policy, authenticated_full_access RLS Policy, Step 1: leads table + RLS, Step 3: Internal Leads module (+20 more)

### Community 6 - "Supabase Client & Login Guard"
Cohesion: 0.12
Nodes (20): login_required(), wrapped(), delete(), index(), upload(), view(), get_supabase(), _add_import_tokens() (+12 more)

### Community 7 - "Homelab n8n, Cloudflare & Google"
Cohesion: 0.12
Nodes (29): Cloudflare (zone gdfacility.com), Cloudflare Access (Zero Trust), Cloudflare Tunnel (gdfacility-homelab), Gmail, Google Voice, Google Workspace, Homelab, n8n (+21 more)

### Community 8 - "Walkthrough Form → submitLead"
Cohesion: 0.14
Nodes (19): Server-only Environment Variables (no NEXT_PUBLIC_ for Supabase), submitLead(), facilityTypes, frequencies, initialLeadFormState, isoDate(), LeadField, LeadFormState (+11 more)

### Community 9 - "Ecosystem Architecture & Deploy"
Cohesion: 0.16
Nodes (20): Walkthrough Form to Supabase Integration (Phase 1), Command Center app, Supabase, Vercel, Company website (gdfacility.com), Company Profile Module, Document Vault (Supabase Storage), AI Contract Command Center Pointer README (+12 more)

### Community 10 - "Flask App Factory & Config"
Cohesion: 0.12
Nodes (6): Config, create_app(), award_note(), fetch_candidates(), main(), pick_closest()

### Community 13 - "Website TypeScript Config"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 14 - "Logo Preparation Script"
Cohesion: 0.11
Nodes (14): best, bg, firstInk, gap, iconBox, iconH, iconW, ink (+6 more)

### Community 15 - "Opportunities List & Past Searches"
Cohesion: 0.17
Nodes (13): list_opportunities(), list_searches(), _local_time(), Search results table partial, Import selected results form, Opportunities tabs partial, Opportunity search & import template, Opportunities list template (+5 more)

### Community 16 - "Website Lint & Package Meta"
Cohesion: 0.14
Nodes (13): eslintConfig, name, private, version, eslint, eslint-config-next, react-dom, tailwindcss (+5 more)

### Community 17 - "Security Review & Dependencies"
Cohesion: 0.15
Nodes (12): HTTP status codes (401 vs 403), flask-limiter, flask-wtf, geopy, tzdata, Auth failure logging, CSRF protection (Flask-WTF), Login error message sanitization (+4 more)

### Community 18 - "Website Brand & Content Brief"
Cohesion: 0.18
Nodes (9): Commercial Cleaning Website Brief, Consultative How-It-Works Process, Local SEO and LocalBusiness Schema, Request a Free Quote / Schedule a Facility Walkthrough CTA, Quote Form Lead Fields, School Cleaning Key Differentiator, WalkthroughForm(), Duplicate-submit Protection (+1 more)

### Community 19 - "Dashboard & Company Profile"
Cohesion: 0.18
Nodes (9): profile(), index(), get_progress_stats(), Sidebar navigation (Phase 1 modules), Company profile template, Company profile form (identity, registration, business), Dashboard template, Phase 1 module summary cards (+1 more)

### Community 20 - "Badge & Video Generation Scripts"
Cohesion: 0.21
Nodes (8): generate(), main(), OUT_DIR, Owner, owners, SHARED, upload(), @higgsfield/client

### Community 21 - "Spam Protection: Honeypot + Turnstile"
Cohesion: 0.25
Nodes (7): Honeypot Field (website), loadScript(), Turnstile(), TurnstileApi, Window, Cloudflare Turnstile, Step 6: Turnstile anti-spam (launch blocker)

### Community 22 - "Website Dev Dependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, puppeteer, sharp, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 23 - "Website npm Scripts"
Cohesion: 0.20
Nodes (10): scripts, badges, build, dev, lint, logo, shots, social (+2 more)

### Community 24 - "CSRF-Protected App Forms"
Cohesion: 0.29
Nodes (10): CSRF protection, Document vault template, Document delete form, Document upload form, Follow-up form, Opportunity detail template, Amendments panel, Delete opportunity form (+2 more)

### Community 26 - "Opportunities Table Migration"
Cohesion: 0.39
Nodes (5): idx_opportunities_agency, idx_opportunities_deadline, idx_opportunities_user, idx_opportunities_user_status, opportunities

### Community 27 - "Website Runtime Dependencies"
Cohesion: 0.25
Nodes (8): dependencies, @higgsfield/client, next, react, react-dom, server-only, @supabase/supabase-js, zod

### Community 28 - "Login & Base Layout"
Cohesion: 0.32
Nodes (6): AdminLTE, login(), logout(), Login template, Login form, Base layout template

### Community 29 - "COMMBUYS Bids Export & Attachments"
Cohesion: 0.25
Nodes (4): CommbuysError, download_attachment(), _fetch_open_bids_export(), get_open_bids()

### Community 30 - "Phase 1 Base Schema"
Cohesion: 0.39
Nodes (7): company_profile, contacts, documents, insurance_bonding, opportunities, past_contracts, pricing_assumptions

### Community 31 - "Opportunities Alignment Migration"
Cohesion: 0.60
Nodes (3): idx_opportunities_agency, idx_opportunities_deadline, idx_opportunities_status

### Community 34 - "Vercel Python Deploy Config"
Cohesion: 0.50
Nodes (3): builds, routes, version

## Ambiguous Edges - Review These
- `createServerSupabase()` → `Supabase anon vs service role key`  [AMBIGUOUS]
  GD_Focus_Solutions/ECOSYSTEM_INTEGRATION.md · relation: conceptually_related_to
- `Command Center app` → `Cleaning Contract Command Center (product vision)`  [AMBIGUOUS]
  GD_Focus_Solutions/PROJECT.md · relation: conceptually_related_to

## Knowledge Gaps
- **118 isolated node(s):** `supabase`, `company_profile`, `pricing_assumptions`, `version`, `builds` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 256 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `createServerSupabase()` and `Supabase anon vs service role key`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Command Center app` and `Cleaning Contract Command Center (product vision)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `get_supabase()` connect `Supabase Client & Login Guard` to `Contracting OS Vision & Opportunity Sourcing`, `Leads Table, RLS & Leads Module`, `Ecosystem Architecture & Deploy`, `Flask Blueprints & Security Libs`, `Opportunities List & Past Searches`, `Dashboard & Company Profile`, `Login & Base Layout`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `Supabase` connect `Ecosystem Architecture & Deploy` to `Contracting OS Vision & Opportunity Sourcing`, `Leads Table, RLS & Leads Module`, `Supabase Client & Login Guard`, `Homelab n8n, Cloudflare & Google`, `Walkthrough Form → submitLead`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `createServerSupabase()` connect `Walkthrough Form → submitLead` to `Ecosystem Architecture & Deploy`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `Supabase leads table` (e.g. with `Quote Form Lead Fields` and `_new_lead_count()`) actually correct?**
  _`Supabase leads table` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `supabase`, `company_profile`, `pricing_assumptions` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._