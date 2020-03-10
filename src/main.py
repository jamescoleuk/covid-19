import alerting #./alerting.py
import checking #./checking.py
import datetime
import gov_uk #./gov_uk.py
import os
import schedule
import time
import yaml


def get_config():
    with open("config.yml", 'r') as config_yaml:
        config = yaml.load(config_yaml, Loader=yaml.FullLoader)
    return config


def get_secrets():
    with open("secrets.yml", 'r') as secrets_yaml:
        secrets = yaml.load(secrets_yaml, Loader=yaml.FullLoader)
    return secrets


def job():
    print("")

    secrets = get_secrets()
    account_sid = secrets["twilio"]["account_sid"]
    auth_token  = secrets["twilio"]["auth_token"]
    from_num = secrets["twilio"]["from_num"]
    to_num = secrets["twilio"]["to_num"]

    config = get_config()
    regions_i_care_about = config["regions"]
    url = config["url"]

    retrieval_time = datetime.datetime.utcnow()
    print(f"Running @ {retrieval_time.isoformat()}")
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    gov_uk.get_c19_stats(url, data_dir, retrieval_time)
    files_to_compare = checking.get_file_names_to_check(data_dir, 0, 1)
    if files_to_compare is not None:
        unchanged, changed = checking.results_for(regions_i_care_about, data_dir, files_to_compare)

        for region in unchanged:
            print(f"  {region}")

        for region in changed:
            print(f"  {region}")

        if(len(changed) > 0):
            message = alerting.get_message(changed)
            alerting.send(message, account_sid, auth_token, from_num, to_num )
    else:
        print("Not enough data to do a comparison yet")


def main():
    config = get_config()
    period_in_minutes = config["check_duration_mins"] 
    print(f"Checking every {period_in_minutes} minutes.")

    job()
    schedule.every(period_in_minutes).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
 
main()