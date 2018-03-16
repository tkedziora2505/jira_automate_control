import mysql.connector

class My_Sql_Database(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='xxx', password='xxxxx!@',
                                           host='127.0.0.1', database='jira_automate_control')
        self.cursor = self.cnx.cursor()

    def add_Task(self, task):
        self.task = task
        self.query = ("INSERT INTO helpline_task(id, create_date, hl_key, hl_name, dead_line, crm_key, check_ok, action)" 
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        self.data = (self.task.id, self.task.create_date, self.task.key, self.task.name, self.task.dd, self.task.crm, "False", 0)
        try:
            self.cursor.execute(self.query, self.data)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE" + str(err))
            return 0

    def check_exist(self, task):
        self.task = task
        print(self.task.id)
        try:
            self.cursor.execute("SELECT * FROM helpline_task WHERE id=%s", (self.task.id,))
            row = self.cursor.fetchone()
            print("Znalazlem na bazie = " + str(row))
            if row != None:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE: " + str(err))
            return False

    def update_Check_Ok(self, task):
        self.task = task
        try:
            self.cursor.execute("UPDATE helpline_task SET check_ok = \"True\" WHERE id=%s", (self.task.id,))
            self.cnx.commit()
            print("Update check_ok ")
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE: " + str(err))


    def update_dd(self, task):
        self.task = task
        try:
            self.cursor.execute("UPDATE helpline_task SET dead_line = %s WHERE id=%s", (self.task.fulldd, self.task.id))
            self.cnx.commit()
            print("Update dd")
        except mysql.connector.Error as err:
            print("ERROR save in DATABASE: " + str(err))
