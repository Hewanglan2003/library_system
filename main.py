import pyodbc
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QLineEdit,QVBoxLayout, QPushButton
from ui.maintable import Ui_MainWindow as Main_Window
from ui.student_info import Ui_MainWindow as Studentinfo_Window
from ui.class_info import Ui_MainWindow as Class_Window
from ui.course_info import Ui_MainWindow as Course_Window
from ui.choice_info import Ui_MainWindow as Choice_Window

#Determine the settings of sql server before connecting
server = "沈雨博"
database = "student_management_system"
username = "shenyubo"
password = "030612"

class MainWindow(QMainWindow, Main_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class StudentWindow(QMainWindow, Studentinfo_Window):
    def __init__(self, cursor):
        super().__init__()
        self.setupUi(self)
        self.cursor = cursor  # 将 cursor 设置为实例变量

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def read_data(self):
        self.clear_table()
        # print("Running query...")
        self.cursor.execute('select * from student')
        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

        # print("Query finished.")


    def search_data(self):
        s_no = self.lineEdit.text()
        s_name = self.lineEdit_2.text()
        s_sex = self.lineEdit_3.text()
        s_age = self.lineEdit_4.text()
        s_classno = self.lineEdit_5.text()
        self.clear_table()

        self.cursor.execute('select * from student where s_no= ? or s_name = ? or s_classno = ?', (s_no, s_name, s_classno))

        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def insert_data(self):
        s_no = self.lineEdit.text()
        s_name = self.lineEdit_2.text()
        s_sex = self.lineEdit_3.text()
        s_age = self.lineEdit_4.text()
        s_classno = self.lineEdit_5.text()
        self.cursor.execute("""
                        MERGE INTO student AS target
                        USING (VALUES (?, ?, ?, ?, ?)) AS source (s_no, s_name, s_sex, s_age, s_classno)
                        ON target.s_no = source.s_no
                        WHEN MATCHED THEN
                            UPDATE SET s_name = source.s_name, s_sex = source.s_sex, s_age = source.s_age, s_classno = source.s_classno
                        WHEN NOT MATCHED THEN
                            INSERT (s_no, s_name, s_sex, s_age, s_classno) VALUES (source.s_no, source.s_name, source.s_sex, source.s_age, source.s_classno);
                    """, (s_no, s_name, s_sex, s_age, s_classno))
        self.cursor.commit()
        self.read_data()

    def delete_data(self):
        s_no = self.lineEdit.text()
        s_name = self.lineEdit_2.text()
        s_sex = self.lineEdit_3.text()
        s_age = self.lineEdit_4.text()
        s_classno = self.lineEdit_5.text()

        self.cursor.execute("delete from student where s_no = ? and s_name  = ?", (s_no, s_name))
        self.cursor.commit()

        self.read_data()

    def update_data(self):
        s_no = self.lineEdit.text()
        s_name = self.lineEdit_2.text()
        s_sex = self.lineEdit_3.text()
        s_age = self.lineEdit_4.text()
        s_classno = self.lineEdit_5.text()

        self.cursor.execute("update student set s_name = ?, s_sex = ?, s_age = ?, s_classno = ? where s_no = ?", (s_name, s_sex, s_age, s_classno, s_no))
        self.cursor.commit()

        self.read_data()

class ClassWindow(QMainWindow, Class_Window):
    def __init__(self, cursor):
        super().__init__()
        self.setupUi(self)

        self.cursor = cursor

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def read_data(self):
        self.clear_table()
        # print("Running query...")
        self.cursor.execute('select * from class')
        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

        # print("Query finished.")

    def search_data(self):
        c_no = self.lineEdit.text()
        c_major = self.lineEdit_2.text()
        c_college = self.lineEdit_3.text()

        self.clear_table()

        self.cursor.execute('select * from class where c_no= ? or c_major = ? ', (c_no, c_major))

        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def insert_data(self):
        c_no = self.lineEdit.text()
        c_major = self.lineEdit_2.text()
        c_college = self.lineEdit_3.text()

        self.cursor.execute("""
                        MERGE INTO class AS target
                        USING (VALUES (?, ?, ?)) AS source (c_no, c_major, c_college)
                        ON target.c_no = source.c_no
                        WHEN MATCHED THEN
                            UPDATE SET c_major = source.c_major, c_college = source.c_college
                        WHEN NOT MATCHED THEN
                            INSERT (c_no, c_major, c_college) VALUES (source.c_no, source.c_major, source.c_college);
                    """, (c_no, c_major, c_college))
        self.cursor.commit()
        self.read_data()

    def delete_data(self):
        c_no = self.lineEdit.text()
        c_major = self.lineEdit_2.text()
        c_college = self.lineEdit_3.text()

        self.cursor.execute("delete from class where c_no = ?", (c_no))
        self.cursor.commit()

        self.read_data()

    def update_data(self):
        c_no = self.lineEdit.text()
        c_major = self.lineEdit_2.text()
        c_college = self.lineEdit_3.text()

        self.cursor.execute("update class set c_major = ?, c_college = ? where c_no = ?", (c_major, c_college, c_no))
        self.cursor.commit()

        self.read_data()

class ChoiceWindow(QMainWindow, Choice_Window):
    def __init__(self, cursor):
        super().__init__()
        self.setupUi(self)

        self.cursor = cursor

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def read_data(self):
        self.clear_table()
        # print("Running query...")
        self.cursor.execute('select * from choice')
        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

        # print("Query finished.")

    def search_data(self):
        ch_student_no = self.lineEdit.text()
        ch_course_no = self.lineEdit_2.text()
        ch_score = self.lineEdit_3.text()

        self.clear_table()

        self.cursor.execute('select * from choice where ch_student_no= ? or ch_course_no = ? ', (ch_student_no, ch_course_no))

        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def insert_data(self):
        ch_student_no = self.lineEdit.text()
        ch_course_no = self.lineEdit_2.text()
        ch_score = self.lineEdit_3.text()

        self.cursor.execute("""
                        MERGE INTO choice AS target
                        USING (VALUES (?, ?, ?)) AS source (ch_student_no, ch_course_no, ch_score)
                        ON target.ch_student_no = source.ch_student_no and target.ch_course_no = source.ch_course_no
                        WHEN MATCHED THEN
                            UPDATE SET ch_score = source.ch_score
                        WHEN NOT MATCHED THEN
                            INSERT (ch_student_no, ch_course_no, ch_score) VALUES (source.ch_student_no, source.ch_course_no, source.ch_score);
                    """, (ch_student_no, ch_course_no, ch_score))
        self.cursor.commit()
        self.read_data()

    def delete_data(self):
        ch_student_no = self.lineEdit.text()
        ch_course_no = self.lineEdit_2.text()
        ch_score = self.lineEdit_3.text()

        self.cursor.execute("delete from choice where ch_student_no = ? and ch_course_no = ?", (ch_student_no, ch_course_no))
        self.cursor.commit()

        self.read_data()

    def update_data(self):
        ch_student_no = self.lineEdit.text()
        ch_course_no = self.lineEdit_2.text()
        ch_score = self.lineEdit_3.text()

        self.cursor.execute("update choice set ch_score = ? where ch_student_no = ? and ch_course_no = ?", (ch_score, ch_student_no, ch_course_no))
        self.cursor.commit()

        self.read_data()

class CourseWindow(QMainWindow, Course_Window):
    def __init__(self, cursor):
        super().__init__()
        self.setupUi(self)
        self.cursor = cursor

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def read_data(self):
        self.clear_table()
        # print("Running query...")
        self.cursor.execute('select * from course')
        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

        # print("Query finished.")


    def search_data(self):
        co_no = self.lineEdit.text()
        co_name = self.lineEdit_2.text()

        self.clear_table()

        self.cursor.execute('select * from course where co_no= ? or co_name = ? ', (co_no, co_name))

        data = self.cursor.fetchall()
        # print("Fetched data:", data)

        self.tableWidget.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def insert_data(self):
        co_no = self.lineEdit.text()
        co_name = self.lineEdit_2.text()
        co_time = self.lineEdit_3.text()
        co_credit = self.lineEdit_4.text()

        self.cursor.execute("""
                        MERGE INTO course AS target
                        USING (VALUES (?, ?, ?, ?)) AS source (co_no, co_name, co_time, co_credit)
                        ON target.co_no = source.co_no
                        WHEN MATCHED THEN
                            UPDATE SET co_name = source.co_name, co_time = source.co_time, co_credit = source.co_credit
                        WHEN NOT MATCHED THEN
                            INSERT (co_no, co_name, co_time, co_credit) VALUES (source.co_no, source.co_name, source.co_time, source.co_credit);
                    """, (co_no, co_name, co_time, co_credit))
        self.cursor.commit()
        self.read_data()

    def delete_data(self):
        co_no = self.lineEdit.text()
        co_name = self.lineEdit_2.text()
        co_time = self.lineEdit_3.text()
        co_credit = self.lineEdit_4.text()

        self.cursor.execute("delete from course where co_no = ? and co_name  = ?", (co_no, co_name))
        self.cursor.commit()

        self.read_data()

    def update_data(self):
        co_no = self.lineEdit.text()
        co_name = self.lineEdit_2.text()
        co_time = self.lineEdit_3.text()
        co_credit = self.lineEdit_4.text()

        self.cursor.execute("update course set co_name = ?, co_time = ?, co_credit = ? where co_no = ?", (co_name, co_time, co_credit, co_no))
        self.cursor.commit()

        self.read_data()

def button_binding(Mainwindow, Studentwindow, Coursewindow, Choicewindow, Classwindow):

    #binding Mainwindow buttons
    Mainwindow.pushButton.clicked.connect(Studentwindow.show)
    Mainwindow.pushButton_2.clicked.connect(Choicewindow.show)
    Mainwindow.pushButton_3.clicked.connect(Classwindow.show)
    Mainwindow.pushButton_4.clicked.connect(Coursewindow.show)

    #binding Studentwindow buttons
    Studentwindow.pushButton.clicked.connect(Studentwindow.read_data)
    Studentwindow.pushButton_2.clicked.connect(Studentwindow.search_data)
    Studentwindow.pushButton_3.clicked.connect(Studentwindow.insert_data)
    Studentwindow.pushButton_4.clicked.connect(Studentwindow.delete_data)
    Studentwindow.pushButton_5.clicked.connect(Studentwindow.update_data)

    #binding Coursewindow buttons
    Coursewindow.pushButton.clicked.connect(Coursewindow.read_data)
    Coursewindow.pushButton_2.clicked.connect(Coursewindow.search_data)
    Coursewindow.pushButton_3.clicked.connect(Coursewindow.insert_data)
    Coursewindow.pushButton_4.clicked.connect(Coursewindow.delete_data)
    Coursewindow.pushButton_5.clicked.connect(Coursewindow.update_data)

    #binding Choicewindow buttons
    Choicewindow.pushButton.clicked.connect(Choicewindow.read_data)
    Choicewindow.pushButton_2.clicked.connect(Choicewindow.search_data)
    Choicewindow.pushButton_3.clicked.connect(Choicewindow.insert_data)
    Choicewindow.pushButton_4.clicked.connect(Choicewindow.delete_data)
    Choicewindow.pushButton_5.clicked.connect(Choicewindow.update_data)

    #binding Classwindow buttons
    Classwindow.pushButton.clicked.connect(Classwindow.read_data)
    Classwindow.pushButton_2.clicked.connect(Classwindow.search_data)
    Classwindow.pushButton_3.clicked.connect(Classwindow.insert_data)
    Classwindow.pushButton_4.clicked.connect(Classwindow.delete_data)
    Classwindow.pushButton_5.clicked.connect(Classwindow.update_data)

class Database():
    def __init__(self, server, database, uid, pwd):
        self.server = server
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.connect = self.sql_server_conn()
        self.cursor = self.connect.cursor()
        print("successful connection")

    def sql_server_conn(self):
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.uid};PWD={self.pwd}'
        connect = pyodbc.connect(connectionString)
        return connect

    def create_table(self):
            self.cursor.execute(
            '''create table student(s_no nchar(20) primary key,s_name nchar(20) not null,s_sex nchar(20) not null check (s_sex = '男' or s_sex = '女'),s_age int not null,s_classno nchar(20) not null)'''
            )

            self.cursor.execute(
            '''create table class(c_no nchar(20) primary key,c_major nchar(20) not null,c_college nchar(20) not null)'''
            )

            self.cursor.execute(
            '''create table choice(ch_student_no nchar(20),ch_course_no nchar(20),ch_score int not null,primary key (ch_student_no, ch_course_no))'''
            )

            self.cursor.execute(
            '''create table course(co_no nchar(20) primary key,co_name nchar(20),co_time int not null,co_credit int not null )'''
            )

            self.cursor.commit()

    def modifying(self):
        self.cursor.execute("drop table course")
        self.cursor.execute('''create table course(co_no nchar(20) primary key,co_name nchar(40),co_time int not null,co_credit int not null )''')
        self.cursor.commit()
        print("successfully modified")

    def operate(self):
        print(123)

if __name__ == '__main__':
    try:
        con = Database(server, database, username, password)
        app = QApplication(sys.argv)

        Mainwindow = MainWindow()
        Studentwindow = StudentWindow(con.cursor)
        Coursewindow = CourseWindow(con.cursor) # add con.cursor
        Choicewindow = ChoiceWindow(con.cursor) #add con.cursor
        Classwindow = ClassWindow(con.cursor)   #add con.cursor

        button_binding(Mainwindow, Studentwindow, Coursewindow, Choicewindow, Classwindow)

        Mainwindow.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"发生错误：{e}")
