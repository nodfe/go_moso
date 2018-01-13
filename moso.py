#coding=UTF-8
import json
import urllib.request
from urllib.parse import urlencode
import zlib
import http.cookiejar
from bs4 import BeautifulSoup
import time
import random
import config

k = config.k
articleId = config.articleId
courseId = config.courseId
sleepNumber = config.sleepNumber
URL_ROOT = config.URL_ROOT
values = config.values
headers = config.headers
subJectUrl = config.subJectUrl

def getOpener():
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    return opener

def getUserInfo(opener):
    data = urlencode(values).encode()
    request = urllib.request.Request(URL_ROOT, data, headers)
    response = opener.open(request)
    print(response.info().get('Content-Encoding'))#输出网页压缩状态
    result_data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)#解压
    mJson = json.loads(result_data)
    print(mJson)
    return mJson

def getSubJectAnswer(opener,userId):
    topic = []
    i = 0
    url = "https://www.mosoteach.cn/web/index.php?c=interaction_quiz&m=person_quiz_result&clazz_course_id=" + courseId + "&id=" + articleId + "&order_item=group&user_id="+userId
    response = opener.open(url)
    html = response.read().decode('utf8')
    mbs = BeautifulSoup(html, "html.parser")
    main_div = mbs.find(attrs={"id": "cc-main"})
    testList_div = main_div.findAll(attrs={"class": "view-quiz-row"})

    for item in testList_div:
        trueRate = item.find(attrs={"style": "color:#07AC6C;"}).string
        title = item.find(attrs={"class": "color-33 topic-subject"}).string
        mDict = {'title': title, 'truerate': trueRate}
        topic.append(mDict)
        i = i + 1
    print("subJectAnswer:" + str(len(topic)))
    return topic

def getSubJect(opener,subJectUrl):
    response = opener.open(subJectUrl)
    result_data = response.read().decode('utf8')
    mbs = BeautifulSoup(result_data, "html.parser")
    main_div = mbs.find(attrs={"id": "cc-main"})
    topics_box = main_div.find(attrs={"id": "topics-box"})
    topicRows = topics_box.findAll(attrs={"class": "student-topic-row"})
    print("topicRows:" + str(len(topicRows)))
    return topicRows

def getRandom(k):
    randomChoice = []
    while (1):
        if k > 0:
            randomNumber = random.randint(0, 99)
            randomChoice.append(randomNumber)
        else:
            break
        k = k - 1
    return randomChoice

def subJectToAnwser(topicRows,answerRows,randomChoice):
    j = 0
    postData = []
    for item in topicRows:
        title = item.find(attrs={"class": "topic-subject"}).string
        data_id = item.attrs['data-id']
        while (1):
            if (answerRows[j]['title'] == title):
                abcdToInteger = {
                    "A": [0],
                    "B": [1],
                    "C": [2],
                    "D": [3]
                }
                if (j in randomChoice):
                    truerate = getABCD(random.randint(0, 3))
                else:
                    truerate = answerRows[j]['truerate']
                trueInt = abcdToInteger[truerate.strip()]
                j = 0
                break
            if (j == 99):
                break
            j = j + 1
        postData.append({"topic_id": data_id, "choice": trueInt})
        j = 0
    return postData

def submit(postData):
    url = "https://www.mosoteach.cn/web/index.php?c=interaction_quiz&m=save_answer"
    time.sleep(sleepNumber)
    postValues = {
        "id": articleId,
        "force": "",
        "data": json.dumps(postData),
        "clazz_course_id": courseId
    }
    data = urlencode(postValues).encode('utf-8')
    response = opener.open(url, data)
    result_data = response.read().decode('utf8')
    print(json.loads(result_data))
    print(u'刷题结束，请打开蓝墨云APP或者蓝墨云Web页面查看！')

def getABCD(integerNumber):
    selectDict = {
        0:"A",
        1:"B",
        2:"C",
        3:"D"
    }
    return selectDict[integerNumber]

opener = getOpener()
userInfo = getUserInfo(opener)
userId = userInfo['user']['user_id']
randomChoice = getRandom(k)
answerRows = getSubJectAnswer(opener,userId)
topicRows = getSubJect(opener,subJectUrl)
postData = subJectToAnwser(topicRows,answerRows,randomChoice)
submit(postData)
