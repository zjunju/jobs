import re


# 将薪资转化为整形，返回月最低和最高工资，默认单位为千/月
def clean_salary(salary_text):
    day_pattern = re.compile(r'(.*?)元/天')
    pattern = re.compile(r'(.*?)-(.*?)([万|千])/([年|月|日])')
    match = re.search(pattern, salary_text)
    try:
        if match:
            highest_salary = float(match.group(2))
            low_salary = float(match.group(1))
            if match.group(4) == '年':
                highest_salary = round(highest_salary / 12, 2)
                low_salary = round(low_salary / 12, 2)
            if match.group(3) == '万':
                highest_salary = highest_salary * 10
                low_salary = low_salary * 10
        else:
            match = re.search(day_pattern, salary_text)
            if match:
                salary = match.group(1)
                highest_salary = float(salary) * 30
                low_salary = highest_salary
            else:
                low_salary, highest_salary =0,0

        return (low_salary, highest_salary)
    except Exception as e:
        print(e)
        return (0,0)


# 清理要求工作时间
def clean_work_time(work_time):
    pattern = re.compile(r'(\d*).*年.*?')
    match = re.search(pattern, work_time)
    if match:
        return match.group(1)
    else:
        return 0

def clean_nusm(nums):
    pattern = re.compile(r'.*?(\d+).*')
    match = re.search(pattern, nums)
    if match:
        return match.group(1)
    else:
        return 0


def clean_job_brief(job_brief):
    try:
        job_brief = [each.strip() for each in job_brief.split("|")]
        region = job_brief[0].strip()
        work_time = job_brief[1].strip()
        edu = job_brief[2].strip()
        nums = job_brief[3].strip()

        num = clean_nusm(nums)
        experience = clean_work_time(work_time)

        return region, experience, edu, num
    except Exception as e:
        print(e)
        return None, None, None, None

