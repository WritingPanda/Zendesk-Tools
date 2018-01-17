from flask import Flask, render_template
from zenpy import Zenpy
import json
import os


app = Flask(__name__)


def get_env_data():
    env = {
        "token": os.environ['ZENDESK_API_KEY'],
        "subdomain": os.environ['ZENDESK_URL'],
        "email": os.environ['ZENDESK_USER'],
    }
    return env

def get_client(token, subdomain, email):
    client = Zenpy(token=token, subdomain=subdomain, email=email)
    return client

def format_results_dates(results):
    for result in results:
        # Adjust the timestamps so they make sense in the CSV (hard-coded nastiness)
        if result["poc_start"] is not None:
            result["poc_start"] = result["poc_start"][0:10]
        if result["poc_expiration_date"] is not None:
            result["poc_expiration_date"] = result["poc_expiration_date"][0:10]
        if result["license_start_date"] is not None:
            result["license_start_date"] = result["license_start_date"][0:10]
        if result["expiration"] is not None:
            result["expiration"] = result["expiration"][0:10]
    return results

def get_organizations(query=None):
    client = get_client(**get_env_data())
    result_list = list()
    for org in client.search(query, type="organization", sort_order="desc"):
        result_list.append({
            "name": org.name,
            "poc_start": org.organization_fields.poc_start,
            "poc_expiration_date": org.organization_fields.poc_expiration_date,
            "license_start_date": org.organization_fields.license_start_date,
            "expiration": org.organization_fields.expiration,
            "license_limit": org.organization_fields.license_limit,
            "type": org.organization_fields.type,
            "location": org.organization_fields.location,
            "partner": org.organization_fields.partner,
            "notes": org.notes,
        })
    formatted_results = format_results_dates(result_list)
    return formatted_results


@app.route("/")
def index():
    results = get_organizations(query="active_poc:true -location:international")
    return render_template("index.html", results=results)


if __name__ == '__main__':
    app.run(debug=True)
