import alerting #./alerting.py
import checking #./checking.py
import datetime
import gov_uk #./gov_uk.py
import schedule
import time
import yaml


def job():
    print("")
    print("Loading secrets from secrets.yml")
    with open("secrets.yml", 'r') as secrets_yaml:
        secrets = yaml.load(secrets_yaml, Loader=yaml.FullLoader)
    account_sid = secrets["twilio"]["account_sid"]
    auth_token  = secrets["twilio"]["auth_token"]
    from_num = secrets["twilio"]["from_num"]
    to_num = secrets["twilio"]["to_num"]

    print("Loading config from config.yml")
    with open("config.yml", 'r') as config_yaml:
        config = yaml.load(config_yaml, Loader=yaml.FullLoader)
    regions_i_care_about = config["regions"]
    url = config["url"]

    retrieval_time = datetime.datetime.utcnow()
    print(f"Running @ {retrieval_time.isoformat()}")
    data_dir = "./data"

    gov_uk.get_c19_stats(url, data_dir, retrieval_time)
    files_to_compare = checking.get_file_names_to_check(data_dir, 0, 1)
    unchanged, changed = checking.results_for(regions_i_care_about, data_dir, files_to_compare)

    for region in unchanged:
        print(f"  {region}")
    
    for region in changed:
        print(f"  {region}")

    if(len(changed) > 0):
        message = alerting.get_message(changed)
        alerting.send(message, account_sid, auth_token, from_num, to_num )


def main():
    period_in_minutes = 60
    print(f"Checking every {period_in_minutes} minutes.")
    job()
    schedule.every(period_in_minutes).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
 
main()