# Automation Service — Main README
# Ready to deploy. Push via gh-pages or Cloudflare Pages once domain is wired.

Welcome to your Automation Service package.

A fixed-price automation contractor starter kit for an Australian sole trader (ABN).

Folders
- `demo-site/` — single-page marketing site (Tailwind via CDN)
- `demo-site/estimator-widget.html` — interactive email/domain savings widget snippet
- `demo-site/faq-process-block.html` — FAQ + 5-step process block snippet
- `workflows/` — lead capture assets (N8N export, Composio script, local POC)
- `contracts/` — client agreement template
- `marketing/` — Upwork profile, finder guide, proposal templates
- `deployment/` — GitHub Pages deploy script
- `backend/` — optional contact form API stub (`contact_api.py`)
- `README.md` — this file

Current status

The site already includes:
- Hero, services, pricing, about, recent-work, contact, footer
- Interactive savings estimator
- FAQ block plus a 5-step process block
- ABN referenced as 71 770 320 895 in the contract
- Proposal templates for Upwork + warm follow-ups

If you want a different brand name, logo, or accent colours, swap them in `demo-site/index.html` and `contracts/krk-automation-agreement.md`.

## Go-live checklist

- [ ] Repo is public or private, depending on your preference
- [ ] GitHub CLI is authenticated for the right account
- [ ] `./deployment/deploy.sh` ran without errors
- [ ] Page is reachable at the expected GitHub Pages URL
- [ ] ABN is correct in the contract
- [ ] Upwork profile is updated
- [ ] First finder emails are queued
- [ ] Bank details / Stripe-ready invoice method are set up for paid work

## Post-launch rhythm

- Push a small site or profile update once a week.
- Send 3–5 finder emails per week.
- If a lead replies, send the demo page plus a fixed-quote draft from `contracts/`.

## Notes

- This kit is ready to use, but real payouts depend on YOU activating Upwork/Stripe/CRM connections and shipping the project.
