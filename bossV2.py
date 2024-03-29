#!/usr/bin/env python3

import json
from urllib import parse
import requests
import sys
import re
import random
import time
import os

jobId = 'a34b94b40f0fa4691HBz0t-7ElE~'

# 获取求职牛人信息列表html
def getJobSeekersList( page, headers ):
    # 这里是你的求职推荐列表
    url = 'https://www.zhipin.com/wapi/zpboss/h5/boss/recommendGeekList?jobid=' + jobId + '&status=0&refresh=1562311420189&source=1&switchJobFrequency=-1&salary=0&age=-1&school=-1&degree=0&experience=0&intention=-1&jobId=' + jobId + '&_=1562311420494&page=' + str(page)
    result = requests.get(url, headers=headers).json()
    jobSeekersList = result['zpData']['geekList']
    return jobSeekersList
# 

# 与牛人打招呼
def greetToJobSeeker( uid, jid, expectId, lid, headers ):
    params = {
        'gids': uid,
        'jids': jid,
        'expectIds': expectId,
        'lids': lid,
    }
    greetResult = requests.post('https://www.zhipin.com/chat/batchAddRelation.json', headers=headers, data=params).json()
    print(greetResult)

# 向牛人发送简历申请
def requestResumeToJobSeeker( uid ):
    requestResumeResult = requests.get('https://www.zhipin.com/chat/requestResume.json?to=' + str(uid) + '&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
    print(requestResumeResult)

# 接受牛人简历
def acceptResumeOfJobSeeker( uid ):
    acceptResumeResuslt = requests.get('https://www.zhipin.com/chat/acceptResume.json?to=' + str(uid) + '&mid=' + str(38834193982) + '&aid=41&action=0&extend=&_=' + str(int(round(time.time() * 1000))), headers=headers).json()
    print(acceptResumeResuslt)

# 获取绝对路径
os.chdir(sys.path[0])
path = os.getcwd()

# 学校排名数据初始化
school985 = []
fSchool985 = open(path + '/985.txt','r')
for line in fSchool985.readlines() :
    school985.append(line.strip())

school211 = []
fSchool211 = open(path + '/211.txt','r')
for line in fSchool211.readlines() :
    school211.append(line.strip())

print(school985)
print(school211)

# 读取本地cookie
f = open(path + '/cookie.txt','r')
cookie = f.readline()
f.close()  

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

loop = True
page = 1
while loop:
    print('--------------------' + str(page))

    # 获取求职牛人信息列表html
    jobSeekersList = getJobSeekersList(page, headers)

    if len(jobSeekersList) < 15:
        loop = False

    for jobSeeker in jobSeekersList :
        # 联系状态
        isFriend = jobSeeker['isFriend']
        if isFriend == 0 :
            contactStatus = "打招呼"
        else :
            contactStatus = "继续沟通"

        jobSeekerInfo = jobSeeker['geekCard']

        # 相关id
        encryptGeekId = jobSeeker['encryptGeekId']#gid
        geekId = jobSeekerInfo['geekId']#uid
        lid = jobSeekerInfo['lid']
        expectId = jobSeekerInfo['expectId']

        # 所在地 杭州
        location = jobSeekerInfo['expectLocationName']
        # 工作年限 5年
        workTime = jobSeekerInfo['geekWorkYear']
        # 学历 本科/硕士
        education = jobSeekerInfo['geekDegree']
        # 年龄 25岁
        age = jobSeekerInfo['ageDesc']
        # 工作状态 在职-考虑机会
        workStatus = jobSeekerInfo['applyStatusDesc']
        # 活跃状态 刚刚活跃
        activeStatus = jobSeeker['activeTimeDesc']
        # 期望薪资
        salary = jobSeekerInfo['salary']
        # 姓名
        name = jobSeekerInfo['geekName']
        # 毕业学校
        school = jobSeekerInfo['geekEdu']['school']

        print('#####' + contactStatus + '#####')
        print('所在地:' + location)
        print('工作年限:' + workTime)
        print('学历:' + education)
        print('年龄:' + age)
        print('求职状态:' + workStatus)
        print('活跃状态:' + activeStatus)
        print('期望薪资:' + salary)
        print('姓名:' + name)
        print('毕业学校:' + school)

        # 学历过滤
        if education == '本科':
            if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 3 :
                print("----------------------------过滤：本科未达到三年----------------------------")
                continue
        elif education == '硕士':
            if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 2 :
                print("----------------------------过滤：硕士未达到两年----------------------------")
                continue
        else:
            print("----------------------------过滤：学历未达到要求----------------------------")
            continue

        # 学校过滤
        hitSchool = False
        for k in school985:
            if school == k:
                hitSchool = True
        for l in school211:
            if school == l:
                hitSchool = True
        if not hitSchool :
            print("----------------------------过滤：学校未达985 OR 211----------------------------")
            continue

        if contactStatus == '打招呼':
            # 与牛人打招呼
            greetToJobSeeker( geekId, jobId, expectId, lid, headers )
        if contactStatus == '继续沟通':
            # 向牛人发送简历申请
            requestResumeToJobSeeker(geekId)
            # 接受牛人简历
            acceptResumeOfJobSeeker(geekId)

    page = page + 1
    randomTime = random.uniform(1,3)
    time.sleep(randomTime)
