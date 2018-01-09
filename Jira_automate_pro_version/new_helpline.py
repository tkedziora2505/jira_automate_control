from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth

from task_abs import Task

class New_Helpline(Task):

    def __init__(self, id, jira):
        self.id = id
        super().__init__(self.id, jira)
        self.jira = jira

    def check_Hl_Is_From_Partner(self):
        if self.groupId == 0:
            return True
        else:
            return False

    def set_Query_By_Name(self):
        self.name = str(self.name).replace("[arh+]", "").replace("[", " ").replace("]", " ").replace("-", " ").replace(":", " ")
        self.queryByResolved    = str('project=HL and status=Resolved and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"")
        self.queryByClosed  = str('project=HL and status=Closed and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"")
        self.queryByVerified = str('project=HL and status=VERIFIED and type="IT: Helpline Incident" and text ~ \"' + str(self.name ) + "\"" + " ORDER BY created DESC")
        self.queryAll = str(self.queryByResolved) + " or " + str(self.queryByClosed) + " or " + str(self.queryByVerified)

    def set_Query_By_Email(self):
        self.queryAll = str('project=CRM and status="Active" and email~"'+str(self.email)+'"')

    def search_Crm_In_Jira(self, queryAll, jira):
        self.crmList = jira.search_issues(queryAll, maxResults=1)
        if len(self.crmList) == 1:
            for crm in self.crmList:
                try:
                    return crm.fields.customfield_11256
                except AttributeError:
                    return crm.key
        else:
            return 0

    def set_Crm(self):
        check = self.check_Hl_Is_From_Partner
        if check == True:
            print("| SYS | Task from Partner")
            self.crmKey = self.search_Crm_In_Jira(self.set_Query_By_Email(self.email), self.jira)
        else:
            print("| SYS | Task from Inside Office")
            self.crmKey = self.search_Crm_In_Jira(self.set_Query_By_Name(), self.jira)

    def accept_Task(self, url):
        self.url = url
        if self.groupId == 4:
            self.data = {'id': self.id, 'customfield_11256': self.crmKey, 'customfield_11213': '10916', 'priority': '1',
                         'customfield_10906': '10723', 'action': '11'}
        else:
            self.data = {'id': self.id, 'customfield_11256': self.crmKey, 'customfield_11213': '10916', 'priority': '4',
                         'customfield_10906': '10723', 'action': '11'}
        cookie = {'atlassian.xsrf.token': 'BJRJ-VNI7-LB9Z-CMCM|8bfa8cac52245131ba165a1e35df9b7b07f4ff38|lin'}
        request = requests.post(self.url, data=self.data, auth=("tkedziora", 'Kedziora02!@'), cookies=cookie)
        return request

    def display(self):
        print(self.__dict__)