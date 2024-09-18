New! Keyboard shortcuts … Drive keyboard shortcuts have been updated to give you first-letters navigation
import os
import requests
import time
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
import urllib3
from datetime import datetime, timezone
urllib3.disable_warnings()
import pandas as pd

def mw_cookie(flags=None, delete_cookie: bool = False):

    # Setting defaults for cookie location
    if flags is None:
        flags = ["-o"]
    cookie_path = "C:\\Users\\name\\.midway\\cookie"

    if delete_cookie:
        os.remove(cookie_path)

    if not os.path.exists(cookie_path):
        os.system(f"mwinit {' '.join(flags)}")

    with open(cookie_path, "rt") as c:
        cookie_file = c.readlines()

    cookies = {}
    # Opening the file and looking at timestamp for expired cookie, running mwinit -o again or getting the cookie
    now = time.time()
    expiration_times = []
    for line in range(4, len(cookie_file)):
        expiration_time = int(cookie_file[line].split("\t")[4])
        expiration_datetime = datetime.fromtimestamp(expiration_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        expiration_times.append(expiration_datetime)
        if expiration_time < now:
            print(f"Cookie expired at {expiration_datetime}. Regenerating using mwinit.")
            os.system(f"mwinit {' '.join(flags)}")
            return mw_cookie(flags=flags)
        cookies[cookie_file[line].split("\t")[5]] = str.replace(
            cookie_file[line].split("\t")[6], "\n", ""
        )
    print("Cookie expiration times:", expiration_times)
    print("Successfully retrieved cookies from file.")
    return cookies

def get_user_input():

    start_date = input("Please enter the start date (YYYY-MM-DD): ")
    end_date = input("Please enter the end date (YYYY-MM-DD): ")
    limit = input("Please enter the limit (number of records to retrieve): ")
    offset = input("Please enter the offset (starting point for retrieval): ")
    process_path = input("Please enter the process path: ")
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "offset": offset,
        "process_path": process_path
    }

def get_pod_number(cookies, params):

    base_url = "anywebsite"
    dashboard_id = "anyname"
    location_name = "anylocation"
    
    # Construct the URL with user-provided parameters
    url = (f"{base_url}?dashboard_id={dashboard_id}&"
           f"end_date={params['end_date']}&"
           f"limit={params['limit']}&"
           f"location_name={location_name}&"
           f"offset={params['offset']}&"
           f"process_path={params['process_path']}&"
           f"start_date={params['start_date']}")
    
    response = requests.get(url, cookies=cookies, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False)
    response.raise_for_status()
 
# Convert the response JSON into a pandas DataFrame
    data = response.json()  # Assuming the API returns JSON
    df = pd.DataFrame(data)
    
    return df

def save_to_csv(df, folder_path="C:\\MyData", filename="output.csv"):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)
    
    df.to_csv(file_path, index=False)
    print(f"Data successfully saved to {file_path}")

if __name__ == "__main__":
    cookies = mw_cookie()
    user_params = get_user_input()
    df = get_pod_number(cookies, user_params)
    save_to_csv(df, folder_path="C:\\MyData")
