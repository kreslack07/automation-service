# Composio Lead Enrichment Script
# Prerequisites: pip install composio-core composio-langchain-openai openai
# Run: python composio-lead-enrichment.py --email user@example.com

import os, sys, json, argparse
from composio_langchain_openai.tools import ComposioToolSet
from composio_langchain_openai.credentials import ComposioCredentials

# Composio App IDs (verify live via composio tools list)
# HubSpot: hubspot, Clearbit: clearbit, Hunter: hunter
HUBSPOT_APP = "hubspot"
CLEARBIT_APP = "clearbit"
GOOGLE_SHEETS_APP = "google_sheets"

# CREDENTIALS: set COMPOSIO_API_KEY env var. Use ~/.openrouter or your api key.
# This script orchestrates: HubSpot create contact, Clearbit enrich, Google Sheets log.

def enrich_and_create(email: str, clearbit_api_key: str = None):
    """
    1. Fetch enrichment data from Clearbit or fallback to a lightweight lookup.
    2. Create / update a HubSpot contact.
    3. Append a log row to Google Sheets.
    
    All API calls are optional; the script is modular so you can skip enrichment.
    """
    tools = ComposioToolSet()
    
    results = {
        "email": email,
        "enriched": False,
        "hubspot_contact_id": None,
        "clearbit": None,
        "sheets_row": None
    }
    
    # 1. Enrichment
    if clearbit_api_key:
        try:
            # Clearbit offers a simple REST enrich endpoint
            import requests
            resp = requests.get(
                "https://person.clearbit.com/v2/combined/find",
                params={"email": email},
                headers={"Authorization": f"Bearer {clearbit_api_key}"}
            )
            if resp.status_code == 200:
                data = resp.json()
                results["enriched"] = True
                results["clearbit"] = data.get("person") or data
            elif resp.status_code == 404:
                results["clearbit_error"] = "no_match"
        except Exception as e:
            results["enriched_error"] = str(e)
    
    # 2. HubSpot Create Contact
    if HUBSPOT_APP:
        try:
            hubspot = tools.get_tools(apps=[HUBSPOT_APP])[0]
            contact = hubspot.run(
                operation="HubSpot.Contacts.Create",
                properties={
                    "email": email,
                    "firstname": results.get("first_name") or "",
                    "lastname": results.get("last_name") or "",
                    "company": results.get("company") or "Unknown"
                }
            )
            results["hubspot_contact_id"] = contact.get("id") or contact.get("objectId")
        except Exception as e:
            results["hubspot_error"] = str(e)
    
    # 3. Google Sheets Log
    if GOOGLE_SHEETS_APP:
        try:
            sheets = tools.get_tools(apps=[GOOGLE_SHEETS_APP])[0]
            row = [
                email,
                results.get("first_name") or "",
                results.get("last_name") or "",
                results.get("company") or "",
                results.get("job_title") or "",
                "true" if results["enriched"] else "false",
                json.dumps(results.get("clearbit") or {})
            ]
            sheets.run(
                operation="Google_Sheets.Add_Row",
                spreadsheetId="YOUR_SPREADSHEET_ID",
                range="Leads_Raw!A1",
                row=row
            )
            results["sheets_row"] = True
        except Exception as e:
            results["sheets_error"] = str(e)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Lead enrichment & CRM pipeline via Composio")
    parser.add_argument("--email", required=True, help="Lead email to enrich")
    parser.add_argument("--clearbit-key", default=None, help="Optional Clearbit API key")
    args = parser.parse_args()
    
    out = enrich_and_create(args.email, args.clearbit_key)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
