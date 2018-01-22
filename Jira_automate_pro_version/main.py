# -*- coding: utf-8 -*-
import json
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
from io import BytesIO
from bs4 import BeautifulSoup
import pycurl
import mysql.connector
import datetime


from task_abs import Task
from first_line import First_Line
from new_helpline import New_Helpline
from second_line import Second_Line
from group_nagios_tasks import Group_Nagios_Tasks
from my_sql_database import My_Sql_Database

def login():
    login = 'tkedziora'
    password = 'Kedziora03!@'
    auth = (login, password)
    return auth

def get_Jira(auth, jiraUrl):
    jira = JIRA(options=jiraUrl, basic_auth=(auth))
    return jira

def get_Tasks_Ids_From_Jira(Tasks_Ids_List, jql_Query, jira):
    search_Task =  jira.search_issues(jql_Query)
    for hl in search_Task:
        Tasks_Ids_List.append(hl.id)
    return Tasks_Ids_List


def send_to_slack(text):
    slack_url = "https://hooks.slack.com/services/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"
    payload = {
        'channel': '#nagios_alert_test',
        'username': 'Jira_Control_Info',
        'icon_emoji': ':information_source:'
    }
    string = text
    payload['text'] = string
    response = requests.post(slack_url, data=json.dumps(payload))
    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))

def get_Page(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.USERPWD, '%s:%s' % ("tkedziora", "Kedziora03!@"))
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    file = buffer.getvalue()
    file = file.decode('utf-8')
    return file

print(str(datetime.datetime.now()))
jiraUrl = {'server': 'https://projects.services.avantis.pl'}
jira = get_Jira(login(), jiraUrl)
NewHlsIdList = []
NewHlsObjectList = []
jql_Query_New_Helpline = 'project=HL and status="New"'
get_Tasks_Ids_From_Jira(NewHlsIdList, jql_Query_New_Helpline, jira)

hlObjectToAcceptList = []
hlObjectFailList = []

if len(NewHlsIdList):
    if len(NewHlsIdList) == 0:
        print("| SYS | Found -> " + str(len(NewHlsIdList)) + " New Task is Jira")
    else:
        print("| SYS | Found -> " + str(len(NewHlsIdList)) + " New Task is Jira")
        for taskId in NewHlsIdList:
            newHlTask = New_Helpline(taskId,jira)
            newHlTask.display()
            newHlTask.set_Crm()
            if newHlTask.crm == 0:
                print("| ERROR | Not Found CRM")
                hlObjectFailList.append(newHlTask)
            else:
                hlObjectToAcceptList.append(newHlTask)

print("| OK | New " + str(len(hlObjectToAcceptList)) + " hl to accept object list -> " + str(hlObjectToAcceptList))
if len(hlObjectFailList) > 1:
    print("| ERROR| New " + str(len(hlObjectFailList)) + " hl with ERROR object list -> " + str(hlObjectFailList))
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

urlPost = 'https://projects.services.avantis.pl/secure/CommentAssignIssue.jspa?atl_token=BJRJ-VNI7-LB9Z-CMCM%7C8bfa8cac52245131ba165a1e35df9b7b07f4ff38%7Clin'
for hl in hlObjectToAcceptList:
    text = str("Zaakceptowalem taska: " + str(hl.key) + " - " + str(hl.name) + " CRM: " + str(hl.crm))
    send_to_slack(text)
    post = hl.accept_Task(urlPost)


FirstLineHlsIdsList = []
FirstLineHlsObjectList = []
jql_Query_Accepted = 'project=HL and status="ACCEPTED - I LINE"'
get_Tasks_Ids_From_Jira(FirstLineHlsIdsList,jql_Query_Accepted,jira)
print("| OK | First line List: " +str(FirstLineHlsIdsList))
if len(FirstLineHlsIdsList) == 0:
    print("| SYS | Found -> " + str(len(FirstLineHlsIdsList)) + " Accepted on Jira - > " + str(FirstLineHlsIdsList))
else:
    print("| SYS | Found -> " + str(len(FirstLineHlsIdsList)) + " Accepted on Jira")
    for taskId in FirstLineHlsIdsList:
        firstLineTask = First_Line(taskId, jira)
        my_sql_Database = My_Sql_Database()
        # print(my_sql_Database.check_exist(firstLineTask))
        if my_sql_Database.check_exist(firstLineTask) == False:
            my_sql_Database.add_Task(firstLineTask)
        # firstLineTask.display()
        elif firstLineTask.check_Time_To_DD() == False:
            firstLineTask.move_To_Second_Line(jira)
            send_to_slack("Przenioslem taska " + str(firstLineTask.key) + " " + str(firstLineTask.name) + " na II linie")
        FirstLineHlsObjectList.append(firstLineTask)
    # print(FirstLineHlsObjectList)

print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

SecondLineHlsIdsList = []
SecondLineHlsObjectList = []
jql_Query_Second_Line = 'project=HL and status="II LINE"'
get_Tasks_Ids_From_Jira(SecondLineHlsIdsList, jql_Query_Second_Line, jira)
print("| OK | Second Line Id List: " +str(SecondLineHlsIdsList))
if len(SecondLineHlsIdsList) == 0:
    print("| SYS | NOT Found -> Second Line on Jira")
else:
    print("| SYS | Found -> " + str(len(SecondLineHlsIdsList)) + " Second Line on Jira")
    for taskId in SecondLineHlsIdsList:
        secondLineTask = Second_Line(taskId, jira)
        secondLineTask.display()
        # print(secondLineTask)
        my_sql_Database = My_Sql_Database()
        # print("Kurwa")
        # print(my_sql_Database.check_exist(secondLineTask))
        if my_sql_Database.check_exist(secondLineTask) == False:
            my_sql_Database.add_Task(secondLineTask)
        # print("TUTAJ == " + str(secondLineTask.fulldd))
        else:
             my_sql_Database.update_dd(secondLineTask)
        if secondLineTask.check_Time_To_DD() == False:
            send_to_slack("DD na II bedzie przekroczony = " + str(secondLineTask.key) + "name = "+ str(secondLineTask.name))
            print("Mam przekroczonego taska na II -> " + str(secondLineTask.key))
        SecondLineHlsObjectList.append(secondLineTask)


allTaskList = FirstLineHlsObjectList + SecondLineHlsObjectList

# print(allTaskList)
for task in allTaskList:
    if task.groupId == 3:
        groupNagiosTask = Group_Nagios_Tasks(task)
        if groupNagiosTask.sure == -1:
            print("| SYS | DELETED -> " + str(groupNagiosTask.hl) + " from nagios group")
            del groupNagiosTask
        else:
            groupNagiosTask.get_Url()
            page = get_Page(groupNagiosTask.url)
            # print(page)
            groupNagiosTask.get_Status(page)
            if groupNagiosTask.check_Ok() == True:
                my_sql_Database.update_Check_Ok(groupNagiosTask)
            if groupNagiosTask.check_ok == True:
                my_sql_Database = My_Sql_Database()
                # print(my_sql_Database.add_Nagios_Tasks(groupNagiosTask))
                send_to_slack("Task " + str(groupNagiosTask.hl) + " jest w stanie OK")
            print("Nagios list: ")
            groupNagiosTask.display()

print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||1")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||2")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||3")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||4")
