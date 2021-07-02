import concurrent.futures
import requests
import threading
import time
import json
import csv

thread_local = threading.local()
result_dic = {}

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    url_1 = 'http://' + url
    url_2 = 'https://' + url
    TIMEOUT = 5
    print(url_1, url_2)
    
    try:
        with session.get(url_1, timeout = TIMEOUT) as response:
            # print(f"Read {len(response.content)} from {url_1}")
            ret_1 = response.status_code
            print(ret_1)
            # result_dic[url_1] = ret_1
    except:
        print('except1')
        ret_1 = 99999
    try:
        with session.get(url_2, timeout = TIMEOUT) as response:
            # print(f"Read {len(response.content)} from {url_2}")
            ret_2 = response.status_code
            print(ret_2)
            # result_dic[url_2] = ret_2
    except:
        print('except2')
        ret_2 = 99999

    if (ret_1 == 200) or (ret_2 == 200):
        ret = 200
    else:
        ret = min(ret_1, ret_2)
    result_dic[url] = ret
    print(ret)

def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(download_site, sites)


if __name__ == '__main__':

    input_sites = []

    with open('source.txt', 'r', encoding='UTF-8') as i_f:
        line = i_f.readlines()
        for web_r in line:
            if web_r =='\n':
                continue
            web = web_r.rstrip('\n')
            input_sites.append(web)
            
        print(input_sites)
        print(len(input_sites))

    # Performance test
    sites = input_sites * 1
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")

    print(result_dic)

    with open('target.csv','w', encoding='utf-8', newline='') as o_f:
        w = csv.writer(o_f)
        for k, v in result_dic.items():
            w.writerow([k, v])