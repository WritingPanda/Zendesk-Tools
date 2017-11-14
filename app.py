"""
Zenpy script -- outputs to CSV
"""


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
        print("Adding {}".format(org.name))
    
    for result in result_list:
        if result[1] is not None:
            result[1] = result[1][0:10]
    
        if result[2] is not None:
            result[2] = result[2][0:10]
    
    return result_list


def write_csv(csv_file, header_row, result_list):
    print("Writing to CSV...")
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(header_row)
        for result in result_list:
            writer.writerow(result)
    print("Finished writing to CSV!")


if __name__ == '__main__':
    import argparse
    import csv
    import os
    from zenpy import Zenpy

    api_token = os.environ['ZENDESK_API_KEY']
    subdomain = os.environ['ZENDESK_URL']
    email_addr = os.environ['ZENDESK_USER']

    zenpy_client = Zenpy(token=api_token, subdomain=subdomain, email=email_addr)

    HELP_TYPE = """
    Type represents either a poc or orgs (all organizations). poc -- license_type:Trial -location:international -- We care about the trial license type that is not associated with an international account. orgs -- No query. This will pull everything from Zendesk and put it to a CSV for us.
    """

    parser = argparse.ArgumentParser(description='Pull data about organizations via Zendesk and save data to a CSV.')
    parser.add_argument('type', type=str, help=HELP_TYPE)
    args = parser.parse_args()

    csv_file = "poc.csv"
    all_orgs_csv_file = "orgs.csv"
    header_row = ["Organization Name", "POC Start", "License Expiration", "License Limit", "Type", "Location", "Partner","Notes"] 

    if args.type == "poc":
        query = "license_type:Trial -location:international"
        result_list = get_organizations_from_zendesk(query)  
        print("Number of POCs: {}".format(len(result_list)))
        write_csv(csv_file, header_row, result_list)
    elif args.type == "orgs":
        query = ""
        result_list = get_organizations_from_zendesk(query) 
        print("Number of POCs: {}".format(len(result_list)))
        write_csv(all_orgs_csv_file, header_row, result_list)
    else:
        print("You must choose poc or orgs.")
