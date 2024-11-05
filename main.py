import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
import sqlite3
import addbook
import addmember
import givebook

con=sqlite3.connect("library.db")
cur=con.cursor()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Library Management')
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.toolbar()
        self.design()
        self.getBooks()
        self.getMembers()
        self.getStatistics()

    def toolbar(self):
        self.tb=self.addToolBar('Tool Bar')
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.add_book=QAction(QIcon('icons/add_book.png'),"Add Book",self)
        self.add_book.triggered.connect(self.addBook)
        self.tb.addAction(self.add_book)
        self.tb.addSeparator()
        #############################################################################
        self.add_member=QAction(QIcon('icons/users.png'),"Add Member",self)
        self.add_member.triggered.connect(self.addMember)
        self.tb.addAction(self.add_member)
        self.tb.addSeparator()
        #############################################################################
        self.give_book=QAction(QIcon('icons/givebook.png'),"Lend Book",self)
        self.give_book.triggered.connect(self.giveBook)
        self.tb.addAction(self.give_book)
        self.tb.addSeparator()


    def design(self):
        ##################in design widgets###########################
        main_layout=QHBoxLayout()
        main_left_layout=QVBoxLayout()
        main_right_layout=QVBoxLayout()
        main_layout.addLayout(main_left_layout,65)
        main_layout.addLayout(main_right_layout,35)
        ######################## tabs ######################################
        self.tabs=QTabWidget(self)
        self.tabs.blockSignals(True)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,'Books')
        self.tabs.addTab(self.tab2,'Members')
        self.tabs.addTab(self.tab3,'Statistics')
        ####################### Tab 1 #################################################
        #################### manin left layout ##############################
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setColumnHidden(0,True)
        self.books_table.setHorizontalHeaderItem(0, QTableWidgetItem("Book ID"))
        self.books_table.setHorizontalHeaderItem(1, QTableWidgetItem("Book Name"))
        self.books_table.setHorizontalHeaderItem(2, QTableWidgetItem("Book Author"))
        self.books_table.setHorizontalHeaderItem(3, QTableWidgetItem("Book Page"))
        self.books_table.setHorizontalHeaderItem(4, QTableWidgetItem("Book Language"))
        self.books_table.setHorizontalHeaderItem(5, QTableWidgetItem("Book Status"))
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        main_left_layout.addWidget(self.books_table)
        ################## main right layout ##############################
            ############# search box #############################
        right_top_frame=QGroupBox(self)
        right_top_frame.setTitle("Search Box")
        right_top_frame.setObjectName("Main")
        right_top_frame.setStyleSheet("#Main{background-color:#9bc9ff;font: 15pt Times Bold;color:white;border:2px solid gray;border-radius:10px;}")
        right_top_frame_box=QHBoxLayout(right_top_frame)
        lbl_search=QLabel("Search",right_top_frame)
        lbl_search.setStyleSheet("font: 13pt Times Bold;color: white;")
        self.search_entry=QLineEdit(right_top_frame)
        self.search_entry.setStyleSheet("border:2px solid gray;border-radius:5px;")
        search_button=QPushButton("Search",right_top_frame)
        search_button.setStyleSheet("background-color:#fcc324;font:13pt Times Bold;color:white")
        search_button.clicked.connect(self.searchBooks)
        right_top_frame_box.addStretch()
        right_top_frame_box.addWidget(lbl_search)
        right_top_frame_box.addWidget(self.search_entry)
        right_top_frame_box.addWidget(search_button)
            #main_right_layout.addLayout(right_top_frame_box,20)
        right_top_frame_box.addStretch()
        main_right_layout.addWidget(right_top_frame,20)
            ############# right side list box #############################
        right_middle_frame=QGroupBox("List Books",self)
        right_middle_frame.setObjectName("Main")
        right_middle_frame.setStyleSheet("#Main{background-color:#fcc324;font:15pt Tİmes Bold;color:white;border:2px solid gray;border-radius:10px;}")
        self.radio_btn1=QRadioButton("All Books",right_middle_frame)
        self.radio_btn2=QRadioButton("Available",right_middle_frame)
        self.radio_btn3=QRadioButton("Borrowed Books",right_middle_frame)
        self.btn_list=QPushButton("List",right_middle_frame)
        self.btn_list.setStyleSheet("background-color:#9bc9ff;font:13pt Times Bold;color:white ")
        self.btn_list.clicked.connect(self.listBooks)
        right_middle_box=QHBoxLayout(right_middle_frame)
        right_middle_box.addStretch()
        right_middle_box.addWidget(self.radio_btn1)
        right_middle_box.addWidget(self.radio_btn2)
        right_middle_box.addWidget(self.radio_btn3)
        right_middle_box.addWidget(self.btn_list)
        right_middle_box.addStretch()
        main_right_layout.addWidget(right_middle_frame,20)
            ############# right side bottom widgets #############################
        right_bottom_layout=QVBoxLayout()
        lbl_title=QLabel("Welcome to Library")
        lbl_title.setContentsMargins(100,0,0,0)
        lbl_title.setFont(QFont('Tİmes',20))
        right_bottom_layout.addWidget(lbl_title)
        img_library=QLabel("")
        img=QPixmap('icons/library.jpg')
        img_library.setContentsMargins(10,0,0,0)
        img_library.setPixmap(img)
        right_bottom_layout.addWidget(img_library)
        main_right_layout.addLayout(right_bottom_layout,60)

        self.tab1.setLayout(main_layout)
    ############# tab1 design done #############################
    ############# tab2 design begin ############################
        member_main_layout=QHBoxLayout()
        member_layout_left=QHBoxLayout()
        member_layout_right=QVBoxLayout()
        member_main_layout.addLayout(member_layout_left,65)
        member_main_layout.addLayout(member_layout_right,35)
        self.members_table=QTableWidget()
        self.members_table.setColumnCount(3)
        self.members_table.setHorizontalHeaderItem(0,QTableWidgetItem("Member ID"))
        self.members_table.setHorizontalHeaderItem(1,QTableWidgetItem("Member Name"))
        self.members_table.setHorizontalHeaderItem(2,QTableWidgetItem("Member Phone"))
        member_layout_left.addWidget(self.members_table)

        member_search_group=QGroupBox("Search Members")
        member_search_group.setObjectName("Main")
        member_search_group.setStyleSheet("#Main{background-color:#fcc324;font:15pt Times Bold;color:white;}")
        member_layout_right_top = QHBoxLayout(member_search_group)
        lbl_member=QLabel("Search")
        self.entry_member_search=QLineEdit()
        button_member_search=QPushButton("Search")
        button_member_search.clicked.connect(self.searchMembers)
        member_layout_right_top.addWidget(lbl_member)
        member_layout_right_top.addWidget(self.entry_member_search)
        member_layout_right_top.addWidget(button_member_search)
        member_layout_right.addWidget(member_search_group)
        member_layout_right.addLayout(member_layout_right_top)
        member_layout_right.addStretch()
        self.tab2.setLayout(member_main_layout)
############ Tab3 Design##############################
        statistic_main_layout=QVBoxLayout()
        self.statistic_group=QGroupBox("Statistics")
        self.statistic_form_layout=QFormLayout()
        self.statistic_group.setFont(QFont("Arial",20))
        self.total_books=QLabel("")
        self.total_members=QLabel("")
        self.taken_books=QLabel("")
        self.available_books=QLabel("")
        self.statistic_form_layout.addChildWidget(self.statistic_group)
        self.statistic_form_layout.addRow(QLabel("Total Books"),self.total_books)
        self.statistic_form_layout.addRow(QLabel("Total Members"),self.total_members)
        self.statistic_form_layout.addRow(QLabel("Taken Books"),self.taken_books)
        self.statistic_form_layout.addRow(QLabel("Available Books"),self.available_books)
        self.statistic_group.setLayout(self.statistic_form_layout)
        statistic_main_layout.addWidget(self.statistic_group)
        self.tab3.setLayout(statistic_main_layout)
        self.tabs.blockSignals(False)

    def tabChanged(self,i):
        self.getMembers()
        self.getStatistics()
        self.getBooks()
    def giveBook(self):
        self.givebook=givebook.GiveBook()
    def addBook(self):
        self.addbook=addbook.AddBook()
    def addMember(self):
        self.addmember=addmember.AddMember()
    def searchMembers(self):
        value=self.entry_member_search.text()
        if value == "":
            QMessageBox.information(self,"Warning","Please enter member name")
        else:
            self.entry_member_search.setText("")
            query=cur.execute("select * from members where member_name like ?", ('%'+value+'%',)).fetchall()
            print(query)
            if query==[]:
                QMessageBox.information(self, "Warning", "There is no such a member")
            else:
                for i in reversed(range(self.members_table.rowCount())):
                    self.members_table.removeRow(i)
                for row_data in query:
                    row_number=self.members_table.rowCount()
                    self.members_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.members_table.setItem(row_number, column_number, QTableWidgetItem(data))

    def getStatistics(self):
        count_books=cur.execute("SELECT count(book_id) FROM books").fetchone()
        count_members=cur.execute("SELECT count(member_id) FROM members").fetchone()
        taken_books=cur.execute("SELECT count(book_status) FROM books WHERE book_status='Not Available'").fetchone()
        available_books=cur.execute("SELECT count(book_status) FROM books WHERE book_status='Available'").fetchone()
        print(taken_books)
        self.total_books.setText(str(count_books[0]))
        self.total_members.setText(str(count_members[0]))
        self.taken_books.setText(str(taken_books[0]))
        self.available_books.setText(str(available_books[0]))



    def getBooks(self):
        self.books_table.setFont(QFont("Times",12))
        query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books")
        for row_data in query:
            row_number=self.books_table.rowCount()
            self.books_table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.books_table.setItem(row_number,column_number,QTableWidgetItem(data))

        self.books_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.books_table.doubleClicked.connect(self.selectedBook)
    def getMembers(self):
        self.members_table.setFont(QFont("Times",12))
        for i in reversed(range(self.members_table.rowCount())):
            self.members_table.removeRow(i)

        query=cur.execute("SELECT * FROM members")
        for row_data in query:
            row_number=self.members_table.rowCount()
            self.members_table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.members_table.setItem(row_number,column_number,QTableWidgetItem(data))

        self.members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.books_table.doubleClicked.connect(self.selectedMember)

    def searchBooks(self):
        value=self.search_entry.text()
        print(value)
        if value =="":
            QMessageBox.information(self,"Warning!!","Search query cant be empty!")
        else:
            query = cur.execute(
                "SELECT book_id, book_name, book_author, book_page, book_language, book_status FROM books "
                "WHERE book_name LIKE ? OR book_author LIKE ?",
                ('%' + value + '%', '%' + value + '%')).fetchall()
            print(query)
            if query == []:
                QMessageBox.information(self,"Warning!!","There is no such a book or author!")
            else:
                for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
                for row_data in query:
                    row_number = self.books_table.rowCount()
                    self.books_table.insertRow(row_number)

                    for column_number,data in enumerate(row_data):
                        self.books_table.setItem(row_number,column_number,QTableWidgetItem(data))

    def listBooks(self):
        print(self.radio_btn1.isChecked())
        if self.radio_btn1.isChecked()==True:
            query=cur.execute("SELECT book_id, book_name, book_author, book_page, book_language, book_status FROM books ")
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(data))

        elif self.radio_btn2.isChecked() == True:
            query=cur.execute("SELECT book_id, book_name, book_author, book_page, book_language, book_status FROM books Where book_status =?",
                              ("Available",))
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(data))

        elif self.radio_btn3.isChecked() == True:
            query = cur.execute(
                "SELECT book_id, book_name, book_author, book_page, book_language, book_status FROM books Where book_status =?",
                ("Not Available",))
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(data))

    def selectedBook(self):
        global book_id
        book_list = []
        for i in range(0,6):
            book_list.append(self.books_table.item(self.books_table.currentRow(),i).text())

        print(book_list)
        book_id=book_list[0]
        self.displaybook = DisplayBook()
        self.displaybook.show()

    def selectedMember(self):
        global member_id
        member_list = []
        for i in range(0,3):
            member_list.append(self.members_table.item(self.members_table.currentRow(),i).text())
        member_id=member_list[0]
        self.displaymember=DisplayBook()
        self.displaymember.show()

class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Member Info')
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 450, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.setStyleSheet("background-color:white;")
        main_layout = QVBoxLayout()
        topFrame = QFrame(self)
        topFrame.setStyleSheet("background-color:white;")
        top_layout = QHBoxLayout(topFrame)
        bottomFrame = QFrame(self)
        bottom_layout = QFormLayout(bottomFrame)
        bottomFrame.setStyleSheet("font:15pt Times Bold;background-color:#fcc324;")

        img_book=QLabel(topFrame)
        img=QPixmap('icons/addbook.png')
        img_book.setPixmap(img)
        lbl_title=QLabel('Add Member',topFrame)
        lbl_title.setStyleSheet("color:#003f8a;font:25pt Times Bold")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        ############# bottom Frame Design ##################################
        self.name_entry=QLineEdit(bottomFrame)
        self.name_entry.setPlaceholderText("Name of Member")
        self.name_entry.setStyleSheet("background-color:white;")
        self.phone_entry=QLineEdit(bottomFrame)
        self.phone_entry.setPlaceholderText("Phone Number")
        self.phone_entry.setStyleSheet("background-color:white;")
        add_button=QPushButton('Add',bottomFrame)
        add_button.clicked.connect(self.addMember)
        bottom_layout.addRow(QLabel('Name:'),self.name_entry)
        bottom_layout.addRow(QLabel('Phone:'),self.phone_entry)
        bottom_layout.addRow(QLabel(""),add_button)
        main_layout.addWidget(bottomFrame)

        self.setLayout(main_layout)

    def addMember(self):
        name=self.name_entry.text()
        phone=self.phone_entry.text()


        if (name and phone !=""):
            try:
                query="INSERT INTO 'members' (member_name,member_phone) VALUES(?,?)"
                cur.execute(query,(name,phone))
                con.commit()
                self.name_entry.setText("")
                self.phone_entry.setText("")
                QMessageBox.information(self,'Information','Member has been added')


            except:
                QMessageBox.information(self,'Warning!!','Member can not be added')

        else:
            QMessageBox.information(self, 'Warning!!', 'Fields can not be empty')

        self.mainpage = main.Main()
        self.mainpage.tabs.Update()

class DisplayBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Display Book')
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 450, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        ########### details from database###################
        global book_id
        book=cur.execute("SELECT * FROM books WHERE book_id=?",(book_id, )).fetchall()
        print(book)
        self.setStyleSheet("background-color:white;")
        main_layout = QVBoxLayout()
        topFrame = QFrame(self)
        topFrame.setStyleSheet("background-color:white;")
        top_layout = QHBoxLayout(topFrame)
        bottomFrame = QFrame(self)
        bottom_layout = QFormLayout(bottomFrame)
        bottomFrame.setStyleSheet("font:15pt Times Bold;background-color:#fcc324;")

        img_book=QLabel(topFrame)
        img=QPixmap('icons/addbook.png')
        img_book.setPixmap(img)
        lbl_title=QLabel('Details of Book',topFrame)
        lbl_title.setStyleSheet("color:#003f8a;font:25pt Times Bold")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        ############# bottom Frame Design ##################################
        self.name_entry=QLineEdit(bottomFrame)
        self.name_entry.setText(book[0][1])
        self.name_entry.setStyleSheet("background-color:white;")
        self.author_entry=QLineEdit(bottomFrame)
        self.author_entry.setText(book[0][2])
        self.author_entry.setStyleSheet("background-color:white;")
        self.page_entry=QLineEdit(bottomFrame)
        self.page_entry.setText(book[0][3])
        self.page_entry.setStyleSheet("background-color:white;")
        self.language_entry=QLineEdit(bottomFrame)
        self.lan_entry.setText(book[0][5])
        self.language_entry.setStyleSheet("background-color:white;")
        self.description=QTextEdit(bottomFrame)
        self.description.setText(book[0][4])
        self.description.setStyleSheet("background-color:white;")
        add_button=QPushButton('Delete',bottomFrame)
        add_button.clicked.connect(self.deleteBook)
        bottom_layout.addRow(QLabel('Name:'),self.name_entry)
        bottom_layout.addRow(QLabel('Author:'),self.author_entry)
        bottom_layout.addRow(QLabel('Page:'),self.page_entry)
        bottom_layout.addRow(QLabel('Language:'),self.language_entry)
        bottom_layout.addRow(QLabel('Description:'),self.description)
        bottom_layout.addRow(QLabel(""),add_button)
        main_layout.addWidget(bottomFrame)



        self.setLayout(main_layout)

    def deleteBook(self):
        global book_id
        mbox=QMessageBox.question(self,"Warning!!","Are you sure to delete this book?",QMessageBox.Yes|QMessageBox.No)
        if mbox==QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM books WHERE book_id=?",(book_id,))
                con.commit()
                QMessageBox.information(self, "Info!!", "Book has been deleted")
                self.main_page = Main()
                self.main_page.tabs.update()
            except:
                QMessageBox.information(self, "Info!!", "Book has not been deleted")


def main():
    App=QApplication(sys.argv)
    window=Main()
    sys.exit(App.exec_())
if __name__ == '__main__':
    main()

