from jira import JIRA
import datetime
class Task(object):

    def __init__(self, id, jira):
        self.id = id
        task = jira.issue(self.id)
        self.name =  str(task.fields.customfield_12902)
        if self.name == "None":
            self.name = str(task.fields.summary)

        self.dd = task.fields.customfield_11267
        self.key = task.key
        self.email = task.fields.customfield_11208
        self.crm = task.fields.customfield_11256
        self.desc = task.fields.description
        if self.email == "arhplus@avantis.pl":
            self.groupId = 1
        elif self.email == "orion@mail.avantis.pl":
            self.groupId = 2
        elif (self.email == "None") or (not self.email):
            self.groupId = 3
        elif self.email == "notify@notify.dotcom-monitor.com":
            self.groupId = 4
        else:
            self.groupId = 0
        pass

    def check_Time_To_DD(self):
        task_DD_String = str(self.dd)
        task_DD_End = task_DD_String.rfind(".")
        task_DD_String = task_DD_String[:task_DD_End]


        date_Now = str(datetime.datetime.now().isoformat())
        date_Now_End = date_Now.rfind(".")
        date_Now = date_Now[: date_Now_End]
        task_DD =  datetime.datetime.strptime(task_DD_String, "%Y-%m-%dT%H:%M:%S")
        date_Now =  datetime.datetime.strptime(date_Now, "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(minutes=15)
        if date_Now < task_DD:
            self.check_Time_To_DD = True
            return self.check_Time_To_DD
        else:
            self.check_Time_To_DD = False
            return self.check_Time_To_DD


