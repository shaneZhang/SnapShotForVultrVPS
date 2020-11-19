#!/usr/bin/env python
# coding=utf8
import json
import httplib2
import time,datetime
import ssl
import requests

########################发送post请求
def sendPostRequest(requesturl,body,api_key):
    try:
        request_headers = {'API-Key':api_key,'Content-type': 'application/x-www-form-urlencoded'}
        ret = requests.post(requesturl,headers=request_headers,data=body)
        content = ret.text
        return content
    except Exception as e:
        print(e)

########################发送Get请求
def sendGetRequest(requesturl,data,api_key):
    try:
        request_headers = {'API-Key':api_key}
        r = requests.get(requesturl,headers=request_headers)
        content = r.text
        return content
    except Exception as e:
        print(e)

#######################################
def createSnapShot(serverid,serverLabel,api_key,subid):
    createSnapShotURL = 'https://api.vultr.com/v1/snapshot/create'
    params = {'SUBID':subid}
    creatResult = sendPostRequest(createSnapShotURL,params,api_key)
    print(creatResult)
    mail_content = '<h5>create snapshot</h5>'
    mail_content += '<p>'
    mail_content += str(creatResult)
    mail_content += '</p>'
    return mail_content

def dropSnapShot(sid,api_key):
    dropSnapShotURL = 'https://api.vultr.com/v1/snapshot/destroy'
    params = {'SNAPSHOTID':sid}
    mail_content = '<h5>drop snapshot</h5>'
    dropResult = sendPostRequest(dropSnapShotURL,params,api_key)
    print(dropResult)
    mail_content += '<p>'
    mail_content += str(dropResult)
    mail_content += '</p>'
    return mail_content

########################################
def snapShotList(api_key):
    snapshotListURL = 'https://api.vultr.com/v1/snapshot/list'
    list = sendGetRequest(snapshotListURL,{},api_key)
    mail_content = '<h5>snapshot list</h5>'
    mail_content += '<p>'
    mail_content += str(list)
    mail_content += '</p>'
    try:
        jsonSnapShotList = json.loads(list)
        snapShotIDList = jsonSnapShotList.keys()
        for snapShotID  in snapShotIDList:
            snapShotInfo = jsonSnapShotList[snapShotID]
            snapShotStatus = snapShotInfo['status']
            snapshotDateCreate = snapShotInfo['date_created']
            logString = str(snapShotID) + ' ' + str(snapShotStatus) + ' ' + str(snapshotDateCreate)
            print(str(logString))
            createDateObject = time.strptime(snapshotDateCreate, "%Y-%m-%d %H:%M:%S")
            y,m,d = createDateObject[0:3]
            calculateTime1 = datetime.date(y,m,d)
            currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            currentTimeObject = time.strptime(currentTime, "%Y-%m-%d %H:%M:%S")
            y1,m1,d1 = currentTimeObject[0:3]
            calculateTime2 = datetime.date(y1,m1,d1)
            calculteDays = ((calculateTime2 - calculateTime1).days)
            print(calculteDays)
            if calculteDays > 5:
                dropLog = dropSnapShot(snapShotID,api_key)
                mail_content += str(dropLog)
    except Exception as e:
        print(e)

    return mail_content

##### post mail#######
def send_Email(content):
    print ('send mailContent')

###############################
if __name__=='__main__':
    api_key = "P6HOBUUTGJSLOQ34G6THW3BF2CRAJSBE64BQ"
    EMAIL_CONTENT = '<h5>run time log:<h5>'
    EMAIL_CONTENT += '<br/>'
    serverURL = 'https://api.vultr.com/v1/server/list'
    serverResult = sendGetRequest(serverURL,{},api_key)
    EMAIL_CONTENT += '<p>'
    EMAIL_CONTENT += str(serverResult)
    EMAIL_CONTENT += '</p>'
    jsonServers = json.loads(serverResult)
    serverIDS = jsonServers.keys()
    for serverID in serverIDS:
        serverInfo = jsonServers[serverID]
        serverLabel = serverInfo['label']
        SUBID = serverInfo['SUBID']
        createLog = createSnapShot(serverID,serverLabel,api_key,SUBID)
        EMAIL_CONTENT += createLog
    #list all the snapshot
    snapListLog = snapShotList(api_key)
    EMAIL_CONTENT += snapListLog
    print (EMAIL_CONTENT)
    send_Email(str(EMAIL_CONTENT))
