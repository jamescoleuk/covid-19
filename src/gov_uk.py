from lxml import html
import csv
import datetime
import requests


def get_c19_stats(url, output_dir, retrieval_time):

    # Why separate files? This data will never get really huge, but it is 
    # the case that for many situations we won't care about very old data.
    # It is also the case that just appending will be a scaling issue, and will
    # result in an increasingly slow program.
    
    # Fetch
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    # Parse to table
    heading_id = "table-of-confirmed-cases-of-covid-19-in-england"
    table_by_heading_path = f'//*[@id="{heading_id}"]/following-sibling::table/tbody/tr'
    cases_table = tree.xpath(table_by_heading_path)
    
    # Extract to dict
    regions = {}
    for row in cases_table:
        region = row[0].text
        cases = row[1].text
        regions[region] = cases
        
    # Write to file
    output_file = f"{output_dir}/{retrieval_time.isoformat()}.csv"
    with open(output_file, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["region", "cases"])
        for key, val in regions.items():
            writer.writerow([key, val])
            
    # Write to a single file
#     output_file = f"./data/all.csv"
#     with open(output_file, "a") as csvfile:
#         writer = csv.writer(csvfile)
#         for key, val in regions.items():
#             writer.writerow([key, val, retrieval_time.isoformat()])


