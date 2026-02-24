import requests
import sys
from bs4 import BeautifulSoup
import json
import re
import zipfile
import warnings
from urllib3.exceptions import InsecureRequestWarning


warnings.filterwarnings('ignore', category=InsecureRequestWarning)

def getIDVersion(searchVersion):
    # use bs4
    headers = {
        'host': 'uupdump.net',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/6.2.5.697',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__itrace_wid=7e01834e-5e27-47f0-0f94-5f832a020f77',
        'referer': 'https://uupdump.net/',
        'priority': 'u=0, i'
    }
    html_content = requests.get(f"https://uupdump.net/known.php?q=category:{searchVersion}",headers=headers,verify=False,allow_redirects=True).text
    # print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find('table', class_='ui celled striped table').find_all('tr')
    target_row = None
    for row in table_rows:
        if row.find('th'):
            continue
        cell_text = row.get_text().lower()
        if 'w11' in searchVersion:
            if 'amd' in cell_text and 'windows 11, version' in cell_text:
                target_row = row
                break
        if 'w10' in searchVersion:
            if 'amd' in cell_text:
                target_row = row
                break
    if target_row:
        link = target_row.find('a')['href']
        uuid = link.split('id=')[1]
        link_text = target_row.text
        version = link_text.split('(')[1].split(')')[0]
        
        # print(f"UUID: {uuid}")
        # print(f"version: {version}")
    else:
        print("not find")

    # use api
    # url = f"https://api.uupdump.net/listid.php?search={searchVersion}&sortByDate=1"
    # res = requests.get(url,verify=False,allow_redirects=True).json()
    # first_build_item = next(iter(res['response']['builds'].values()))
    # version = first_build_item['build']

    # url = f"https://api.uupdump.net/listid.php?search={version}&sortByDate=1"
    # res = requests.get(url,verify=False,allow_redirects=True).json()
    # res =iter(res['response']['builds'].values())
    # for i in res:
    #     if i['arch'] == "amd64":
    #         uuid = i['uuid']

    return uuid,version



def download_file(uuid):
    headers = {
        'host': 'uupdump.net',
        'content-length': '78',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://uupdump.net',
        #'x-uctiming-46938875': '1769004852407',
        'upgrade-insecure-requests': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/6.2.5.697',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__itrace_wid=7e01834e-5e27-47f0-0f94-5f832a020f77',
        #'referer': f'https://uupdump.net/download.php?id={uuid}&pack=en-us&edition=professional',
        'priority': 'u=0, i'
    }
    data = "autodl=3&updates=1&cleanup=1&netfx=1&esd=1&virtualEditions%5B%5D=IoTEnterprise"
    url = f"https://uupdump.net/get.php?id={uuid}&pack=en-us&edition=professional"
    response = requests.post(url,headers=headers,data=data,verify=False)
    response.raise_for_status()

    with open("a.zip", 'wb') as file:
        file.write(response.content) 

    # print(f"done.")


def unzip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_obj:
        zip_obj.extractall(path='./')

def main():
    uuid,version = getIDVersion(sys.argv[1])
    # uuid,version = getIDVersion("26h1")
    # print(uuid)
    # print(version)
    # uuid = "0e1cec91-9bb2-41ad-929f-fe36a5beda02"
    # version = '28000.1450'
    download_file(uuid)
    unzip("a.zip")
    print(version)

if __name__ == '__main__':
    main() 
