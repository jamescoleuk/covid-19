from os import listdir
from os.path import isfile, join
import datetime
import pandas as pd


def get_file_names_to_check(output_dir, a_index, b_index):
    files = [f for f in listdir(output_dir) if isfile(join(output_dir, f))]
    files.sort(reverse=True)
    return [files[a_index], files[b_index]]


def check_for(region, data_dir, a_file_name, b_file_name):
    a = pd.read_csv(f"{data_dir}/{a_file_name}")
    b = pd.read_csv(f"{data_dir}/{b_file_name}")

    a_count = a.loc[a["region"] == region]["cases"].item()
    b_count = b.loc[b["region"] == region]["cases"].item()
    
    return [a_count, b_count]


def results_for(regions_i_care_about, data_dir, files_to_compare):
    unchanged = []
    changed = []
    for region in regions_i_care_about:
        counts = check_for(region, data_dir, files_to_compare[0], files_to_compare[1])
        has_changed = counts[0] != counts[1]
        if has_changed:
            message_body = f"{region} has changed from {counts[1]} to {counts[0]}"
            changed.append(message_body)
        else:
            unchanged.append(f"{region} has not changed, is still {counts[1]}")
    
    return [unchanged, changed]


