import pyodbc
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QLineEdit,QVBoxLayout, QPushButton
from ui.maintable import Ui_MainWindow as Main_Window
from ui.student_info import Ui_MainWindow as Studentinfo_Window
from ui.class_info import Ui_MainWindow as Class_Window
from ui.course_info import Ui_MainWindow as Course_Window
from ui.choice_info import Ui_MainWindow as Choice_Window

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
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ChoiceWindow(QMainWindow, Choice_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class CourseWindow(QMainWindow, Course_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        Coursewindow = CourseWindow() # add con.cursor
        Choicewindow = ChoiceWindow() #add con.cursor
        Classwindow = ClassWindow()   #add con.cursor

        button_binding(Mainwindow, Studentwindow, Coursewindow, Choicewindow, Classwindow)

        Mainwindow.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"发生错误：{e}")
