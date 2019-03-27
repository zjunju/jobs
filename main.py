import re
import html
import pymysql
import requests
from pyquery import PyQuery

import utils
import get_jobs
from mysql_settings import MySettings


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

db = pymysql.connect(host=MySettings.HOST, user=MySettings.USER, password=MySettings.PASSWORD, port=3306, db=MySettings.DB_NAME)
cursor = db.cursor()
db.close()

# 获取所有url
with open('jobs_url.txt') as fo:
    lines = fo.readlines()[0]
    jobs_url = lines.split(',')

done_jobs_url = []
error_jobs_url = []

try:
    for url in jobs_url:
        print(url)
        response = requests.get(url, headers=headers)
        salary_pattern = re.compile(r'.*?(.*?)-(.*?)[万|千]')
        if response.status_code == 200:
            pq_obj = PyQuery(response.text)
            # 得到关于职位信息的div
            job_info_div = pq_obj('div.cn')

            # 获取各种信息
            job_name = job_info_div('h1').text()  # 职位名称
            salary_range = job_info_div('strong').text()    # 薪资范围
            low_salary, highest_salary = utils.clean_salary(salary_range)   # 清理后的薪资
            address = pq_obj('p.fp').text()
            # 工作信息拆分成几个部分 区域 要求工作经验 学历 招人数
            # 如果exprience为0则表示不需要工作经验， num为0则表示招若干人
            job_brief = pq_obj('p.msg.ltype').text()
            region, experience, edu, nums = utils.clean_job_brief(job_brief)

            company = pq_obj('p.cname a.catn').text()       #  公司名称
            job_info = pq_obj('div.bmsg.job_msg.inbox').text()  # 工作详细信息
            company_info = pq_obj('div.tmsg.inbox').text()      # 公司信息
            # 获取当前的url
            url = response.url

            # 创建data字典，保存所有要插入到数据库表中的数据
            data = {
                "company": company,
                'job_name': job_name,
                'job_info': job_info,
                'region': region,
                'experience': experience,
                'edu': edu,
                'nums': nums,
                'url': url,
                'job_name': job_name,
                'company_info': company_info,
                'low_salary': low_salary,
                'highest_salary': highest_salary,
                'address': address
            }

            # 要插入的列的值
            columns = ','.join(data.keys())
            # 添加%s
            values = ",".join(['%s']*len(data))

            # 创建sql插入数据语句
            sql = 'INSERT INTO jobs({0}) VALUES ({1})'.format(columns, values)
            try:
                cursor.execute(sql, list(data.values()))
                db.commit()
                done_jobs_url.append(url)
            except  Exception as e:
                print(e)
                print(e.with_traceback())
                error_jobs_url.append(url)
                db.rollback()
        else:
            response.status_code
finally:
    db.close()
    with open('done_jobs_url.txt', 'w+', encoding='utf-8') as fo:
        fo.write(','.join(done_jobs_url))
    with open('error_jobs_url.txt', 'w+', encoding='utf-8') as fo:
        fo.write(','.join(error_jobs_url))

