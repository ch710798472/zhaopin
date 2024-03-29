#!/usr/bin/env python3

import json
from urllib import parse
import bs4
import requests
import sys
import re
import random
import time
import os
import traceback

jobId = '-1'

# 获取求职牛人信息列表html
def getJobSeekersHtml( page, headers ):
    # 这里是你的求职推荐列表
    url = 'https://www.zhipin.com/boss/recommend/geeks.json?status=0&jobid=' + jobId + '&salary=-1&experience=-1&degree=-1&intention=-1&_=1556612495320&page=' + str(page)
    result = requests.get(url, headers=headers).json()
    html = result['htmlList']
    return html

# https://www.zhipin.com/wapi/zpboss/h5/boss/recommendGeekList?jobid=9488aeda0e36a75203Ry39-9F1c~&status=0&refresh=1562311420189&source=1&switchJobFrequency=-1&salary=0&age=-1&school=-1&degree=0&experience=0&intention=-1&jobId=9488aeda0e36a75203Ry39-9F1c~&page=1&_=1562311420494

# 与牛人打招呼
def greetToJobSeeker( uid, jid, expectId, lid, suid, headers ):
    params = {
        'gids': uid,
        'jids': jid,
        'expectIds': expectId,
        'lids': lid,
        'suids': suid
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

oldName = []
fOldName = open(path + '/old.txt','r')
for line in fOldName.readlines() :
    oldName.append(line.strip())

wOldName = open(path + '/old.txt','a')

exceptJobName = []
fJobName = open(path + '/jobName.txt','r')
for line in fJobName.readlines() :
    exceptJobName.append(line.strip())

print(school985)
print(school211)
print(oldName)

# 读取本地cookie
f = open(path + '/cookie.txt','r')
cookie = f.readline()
f.close()  
print(cookie)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'toUrl=/; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1562758616; __g=-; t=tPWG3RPrfhcAgtTs; wt=tPWG3RPrfhcAgtTs; __c=1562758765; __l=r=https%3A%2F%2Fwww.zhipin.com%2Fuser%2Flogin.html&l=%2Fwww.zhipin.com%2Fchat%2Fim; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1562759486; __a=21059410.1562758616.1562758616.1562758765.5.2.4.5',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

loop = True
page = 1
while loop:
    print('--------------------' + str(page))

    # 获取求职牛人信息列表html
    html = getJobSeekersHtml(page, headers)

    soup = bs4.BeautifulSoup(html, 'html.parser')

    if len(soup.find_all('li')) < 15:
        loop = False

    for li in soup.find_all('li') :
        try:
            # 联系状态
            contactStatusButton = li.find('div', attrs={'class': 'sider-op'}).find('button', attrs={'class': 'btn btn-greet'})
            if contactStatusButton is None:
                contactStatusButton = li.find('div', attrs={'class': 'sider-op'}).find('button', attrs={'class': 'btn btn-continue'})
                if contactStatusButton is None:
                    contactStatus = '无'
                else:
                    contactStatus = contactStatusButton.string
            else:
                contactStatus = contactStatusButton.string

            # 牛人
            a = li.find('a')
            # 相关id
            uid = a['data-uid']
            suid = a['data-suid']
            jid = a['data-jid']
            lid = a['data-lid']
            expectId = a['data-expect']

            # 个人基本信息区块1
            div1 = a.find('div', attrs={'class': 'info-labels'})
            spanList = div1.find_all('span', attrs={'class': 'label-text'})
            # 所在地 杭州
            location = spanList[0].string
            # 工作年限 5年
            workTime = spanList[1].string
            # 学历 本科/硕士
            education = spanList[2].string
            # 年龄 25岁
            age = ''
            if (len(spanList) >= 4) :
                age = spanList[3].string
            # 工作状态 在职-考虑机会
            workStatus = ''
            if (len(spanList) >= 5) :
                workStatus = spanList[4].string
            # 活跃状态 刚刚活跃
            if (len(spanList) >= 6) :
                activeStatus = spanList[5].string
            else :
                activeStatus = '无'

            # 个人基本信息区块2
            div2 = a.find('div', attrs={'class': 'chat-info'})
            # 期望薪资
            salary = div2.find('div', attrs={'class': 'figure'}).find('span', attrs={'class': 'badge-salary'}).string
            # 姓名
            name = div2.find('div', attrs={'class': 'text'}).find('span', attrs={'class': 'geek-name'}).string
            # 求职期望
            if div2.find('div', attrs={'class': 'text'}).find('p') is None :
                exceptList = '无'
            else:
                exceptList = div2.find('div', attrs={'class': 'text'}).find('p').get_text()
            # if re.search(r"Java", exceptList) is None:
            #     continue
            hitJob = False
            for jobName in exceptJobName:
                if exceptList.find(jobName) != -1:
                    hitJob = True
            if not hitJob :
                print("过滤：期望职位不符" + exceptList)
                continue


            # 工作经历
            if div2.find('div', attrs={'class': 'text'}).find('p', attrs={'class': 'experience'}) is None :
                experience = '无'
            else :
                experience = div2.find('div', attrs={'class': 'text'}).find('p', attrs={'class': 'experience'}).get_text().strip()
            # 毕业学校
            school = div2.find('div', attrs={'class': 'text'}).find_all('p')[2].get_text().strip()

            # 学历过滤
            if re.search(r"[0-9]{1,2}", workTime) is not None:
                if education == '本科':
                    if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 3 :
                        print("过滤：本科未达到三年")
                        continue
                elif education == '硕士':
                    if int(re.search(r"[0-9]{1,2}", workTime).group(0)) < 2 :
                        print("过滤：硕士未达到两年")
                        continue
                else:
                    print("过滤：学历未达到要求")
                    continue
            else:
                print("过滤：学历未达到要求")
                continue
            if re.search(r"应届生", workTime) is not None:
                continue

            # 学校过滤
            hitSchool = False
            print(school)
            for k in school985:
                if school.find(k) != -1:
                    hitSchool = True
            for l in school211:
                if school.find(l) != -1:
                    hitSchool = True
            if not hitSchool :
                print("过滤：学校未达985 OR 211")
                continue

            for old_name in oldName:
                if name.find(old_name) != -1:
                    continue
            wOldName.write(name + "\n")
            print('#####' + contactStatus + '#####')
            print('所在地:' + location)
            print('工作年限:' + workTime)
            print('学历:' + education)
            print('年龄:' + age)
            print('求职状态:' + workStatus)
            print('活跃状态:' + activeStatus)
            print('期望薪资:' + salary)
            print('期望岗位:' + exceptList)
            print('姓名:' + name)
            print('工作经历:' + experience)
            print('毕业学校:' + school)

            if contactStatus == '打招呼':
                # 与牛人打招呼
                greetToJobSeeker(uid, jid, expectId, lid, suid, headers)
            if contactStatus == '继续沟通':
                # 向牛人发送简历申请
                requestResumeToJobSeeker(uid)
                # 接受牛人简历
                acceptResumeOfJobSeeker(uid)
        except Exception as e:
            print("except error")
            info = traceback.format_exc()
            print(info)

    page = page + 1
    randomTime = random.uniform(1,3)
    time.sleep(randomTime)
wOldName.close()
