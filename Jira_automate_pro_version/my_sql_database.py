import mysql.connector

class My_Sql_Database(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='kociak2003!@',
                                           host='127.0.0.1', database='jira_control_automate')
        self.cursor = self.cnx.cursor()

    def add_Nagios_Tasks(self, nagios_Task):
        self.nagios_Task = nagios_Task
        self.query = ("INSERT INTO nagios_tasks(id, hl, check_ok) " 
                            "VALUES (%s, %s, %s)")
        self.data = (self.nagios_Task.id, self.nagios_Task.hl, self.nagios_Task.check_ok)
        try:
            self.cursor.execute(self.query, self.data)
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE" + str(err))
            return 0

    def add_Accepted_Task(self, accepted_task):
        self.accepted_Task = accepted_task
        self.query = ("INSERT INTO accepted_tasks(id, hl, name, crm, email, groupId, descri) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        self.data = (self.accepted_Task.id, self.accepted_Task.key, self.accepted_Task.name, self.accepted_Task.crm, self.accepted_Task.email, self.accepted_Task.groupId, self.accepted_Task.desc)
        try:
            self.cursor.execute(self.query, self.data)
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE" + str(err))
            return 0

    def error(self):
        try:
            self.cursor.execute(self.query, self.data)
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE" + str(err))
            return 0

