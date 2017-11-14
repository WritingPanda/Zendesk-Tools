from flask import Flask, render_template
from zenpy import Zenpy
import os


app = Flask(__name__)
api_token = os.environ['ZENDESK_API_KEY']
subdomain = os.environ['ZENDESK_URL']
email_addr = os.environ['ZENDESK_USER']
zenpy_client = Zenpy(token=api_token, subdomain=subdomain, email=email_addr)

def get_organizations_from_zendesk(query):
    result_list = list()
    for org in zenpy_client.search(query, type="organization", sort_by="created_at", sort_order="desc"):
        result_list.append([
            org.name, 
            org.organization_fields.poc_start, 
            org.organization_fields.expiration,
            org.organization_fields.license_limit,
            org.organization_fields.type,
            org.organization_fields.location,
            org.organization_fields.partner,
            org.notes
        ])
    
    for result in result_list:
        # Adjust the timestamps so they make sense in the CSV (hard-coded nastiness)
        if result[1] is not None:
            result[1] = result[1][0:10]
        if result[2] is not None:
            result[2] = result[2][0:10]
    return result_list


results = get_organizations_from_zendesk("license_type:Trial -location:international")

@app.route("/")
def index():
    return render_template("index.html", results=results)


if __name__ == '__main__':
    app.run(debug=True)
