from jira import JIRA
from task_abs import Task

class Second_Line(Task):

    def __init__(self, id, jira):
        self.id = id
        self.jira = jira
        super(Second_Line, self).__init__(self.id, jira)

    def check_Time_To_DD(self):
        task = self.jira.issue(self.id)
        self.dd = task.fields.customfield_11268
        check_Time_To_DD = Task.check_Time_To_DD(self)
        return check_Time_To_DD

    def display(self):
        print(self.__dict__)