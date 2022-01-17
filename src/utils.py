from operator import index
import os
import requests


def get_indexes_files():

    path = f"./src/indexes/"

    indexes_files = [path+file  for file in os.listdir(path)]

    return indexes_files


def export_faq_csv(df_out, name):

    path = f"./data"

    if not os.path.isdir(path):
        os.makedirs(path)

    df_out.to_csv(f"{path}/{name}_faq.csv")


def upload_faq_files(index):

    host = os.getenv("FRANK_HOST", "askfrank.ai")
    port = os.getenv("FRANK_PORT", "5000")
    route = "/update_faq"

    ## Create the URL
    url = f"https://{host}:{port}{route}"

    max_attempts = 3

    payload = {}
    files = [("file",(index["faq_name"],open(f"./data/{index['faq_name']}","rb"),"text/csv"))]
    headers = {
        'auth_code': index["auth_code"],
        'x-access-token': index["token"]
    }

    ## Try max_attempts times before to return
    attempts = 0
    while True:
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        if (response.status_code == 200 ) or (attempts >= max_attempts):
            break
        else:
            attempts += 1

    print(response.status_code, response.content)
    return response.status_code, response.content

if __name__ == "__main__":

    get_index_files()