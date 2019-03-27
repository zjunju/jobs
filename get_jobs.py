import re
import time
import requests
from pyquery import PyQuery


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}



def get_page_job_hrefs(page_url):
    hrefs = []
    response = requests.get(page_url, headers=headers)
    response.encoding = None
    if response.status_code == 200:
        pq_obj = PyQuery(response.text)
        pq_obj.find('div.dw_table div.el.title').remove()
        all_e1 = pq_obj('div.dw_table div.el')
        for each in all_e1.items():
            hrefs.append(each('a').attr('href'))
    else:
        print('error：  ', page_url)

    return hrefs


def run(max_page=10):
    url = "https://search.51job.com/list/040000,000000,0000,00,9,99,Python,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=21&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    max_page += 1
    all_hrefs = []
    with open('jobs_url.txt', 'w+', encoding="utf-8") as fo:
        for i in range (1, max_page):
            page_url = url.format(i)
            hrefs = get_page_job_hrefs(page_url)
            time.sleep(3)
            all_hrefs.append(hrefs)
            print(hrefs)
            fo.write(",".join(hrefs))
            print(i, 'done')

    return all_hrefs

"""
response =requests.get(url%5)
response.encoding = None
if response.status_code == 200:
    print(response.text)
else:
    print('error')
"""