from jira import JIRA
from task_abs import Task

class First_Line(Task):
    def __init__(self, id, jira):
        self.id = id
        self.jira = jira
        super(First_Line, self).__init__(self.id, jira)

    def check_Time_To_DD(self):
        check_Time_To_DD = Task.check_Time_To_DD(self)
        # print(check_Time_To_DD)
        return check_Time_To_DD

    def move_To_Second_Line(self, jira):
        issue = jira.issue(self.id)
        jira.assign_issue(issue, 'tkedziora')
        transitions = jira.transitions(issue)
        jira.transition_issue(issue, '161')

    def display(self):
        print(self.__dict__)
