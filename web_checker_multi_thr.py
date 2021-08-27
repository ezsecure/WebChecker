import concurrent.futures
import requests
import threading
import datetime
import time
import csv
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

thread_local = threading.local()
result_dict = {}

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    session = get_session()
    url_1 = 'http://' + url
    url_2 = 'https://' + url
    ret_1 = 99999
    ret_2 = 99999
    TIMEOUT = 10
    # print(url_1, url_2)

    try:
        # allow_redirects = True 이면 redirect되어 최종 status_code가 확인됨
        with session.get(url_1, verify = False, timeout = TIMEOUT, allow_redirects = True) as response:
            # print(f"Read {len(response.content)} from {url_1}")
            ret_1 = response.status_code
            print(url_1, ret_1)
            # result_dic[url_1] = ret_1
    except:
        print(url_1, 'except1')
        ret_1 = 99999

    try:
        with session.get(url_2, verify = False, timeout = TIMEOUT, allow_redirects = True) as response:
            # print(f"Read {len(response.content)} from {url_2}")
            ret_2 = response.status_code
            print(url_2, ret_2)
            # result_dic[url_2] = ret_2
    except:
        print(url_2, 'except2')
        ret_2 = 99999

    if (ret_1 == 200) or (ret_2 == 200):
        ret = 200
    else:
        ret = min(ret_1, ret_2)
    result_dict[url] = ret
    # print(ret)

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

    # 시작, 종료시간 측정하여 Thread기반 웹호출
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")

    print(result_dict)

    # 2021.07.20 응답코드 비교 로직 추가

    # check file lists in this directory
    path = "./"
    file_list = os.listdir(path)
    # print (file_list)

    # Result로 시작되는 파일 추출하여 마지막 진단 결과 파일 고르기 -> compare_origin 이름으로 정의
    result_list = []
    for i in file_list:
        if i.startswith("Result-") :
            result_list.append(i)

    if not result_list :
        init = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        output_filename = 'Result-' + init + '.csv'
        with open(output_filename, 'w'):
            pass
        file_list = os.listdir(path)
        for i in file_list:
            if i.startswith("Result-") :
                result_list.append(i)


    compare_origin = max(result_list)
    # print(result_list)
    print('Baseline for Comparison : ' + compare_origin)

    comp_list = []
    with open(compare_origin, 'r', encoding='UTF-8', newline='') as i_f_diff:
        w = csv.reader(i_f_diff)
        for row in w:
            idx = row[0]
            if idx in result_dict.keys():
                # 코드가 같을 때 저장하려면 부등호를 등호로 변경필요
                if int(row[1]) != int(result_dict[idx]):
                    temp_list = [idx, row[1], result_dict[idx]]
                    comp_list.append(temp_list)
    print(comp_list)

    # check present time
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    print('Now : ' + now)
    output_filename = 'Result-' + now + '.csv'
    diff_filename = 'Diff-' + now + '.csv'

    with open(output_filename,'w', encoding='utf-8', newline='') as o_f:
        w = csv.writer(o_f)
        for k, v in result_dict.items():
            w.writerow([k, v])

    with open(diff_filename,'w', encoding='utf-8', newline='') as o_f:
        w = csv.writer(o_f)
        w.writerows(comp_list)