import os
import requests

def export_faq_csv(df_out, name):

    path = f'./data'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_out.to_csv(f'{path}/{name}_faq.csv')


def post_files(gender):

    url = "https://askfrank.ai:5000/update_faq"

    payload={}
    files=[
    ("file",(gender["file_name"],open(f"./data/{gender['file_name']}","rb"),"text/csv"))
    ]
    headers = {
    'auth_code': gender["auth_code"],
    'x-access-token': gender["token"]
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)