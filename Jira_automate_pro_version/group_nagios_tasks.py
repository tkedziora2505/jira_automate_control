from io import BytesIO
from bs4 import BeautifulSoup

class Group_Nagios_Tasks(object):
    def __init__(self, task):
        self.nagios_Task = task
        self.hl = self.nagios_Task.key
        self.id = self.nagios_Task.id
        # print(self.sure)
        self.check_ok = False
        self.sure = int(str(self.nagios_Task.name).find("Nagios"))

    def get_Url(self):
        self.url = str(self.nagios_Task.desc)
        urlStart = self.url.rfind("Check:")+7
        urlEnd = self.url.rfind("Wiki")-1
        self.url = self.url[urlStart:urlEnd]

    def display(self):
        print(self.__dict__)

    def get_Status(self, file):
        info = BeautifulSoup(file, "html.parser")
        classList = ["serviceCRITICAL", "serviceOK", "serviceWARNING"]
        for row in info.find(class_=classList):
            self.status = str(row).strip()

    def check_Ok(self):
        # print(self.status)
        # print(type(self.status))
        if self.status == "OK":
            self.check_ok = True

