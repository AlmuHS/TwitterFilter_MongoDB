# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QHBoxLayout
import sys
import time

import mongodb_manager as MDBMan


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.horizontal_layout = QHBoxLayout()
        self.setLayout(self.horizontal_layout)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 838)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(771, 16777215))
        self.centralwidget.setObjectName("centralwidget")

        self.search_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.search_pushButton.setGeometry(QtCore.QRect(150, 400, 88, 27))
        self.search_pushButton.setObjectName("pushButton")
        self.collection_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.collection_comboBox.setGeometry(QtCore.QRect(140, 50, 191, 27))
        self.collection_comboBox.setObjectName("collection_comboBox")
        self.collections_label = QtWidgets.QLabel(self.centralwidget)
        self.collections_label.setGeometry(QtCore.QRect(50, 50, 91, 19))
        self.collections_label.setObjectName("collections_label")
        self.daterange_checkBox = QtWidgets.QRadioButton(self.centralwidget)
        self.daterange_checkBox.setGeometry(QtCore.QRect(150, 190, 131, 25))
        self.daterange_checkBox.setObjectName("daterange_checkBox")
        self.kwplainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.kwplainTextEdit.setGeometry(QtCore.QRect(150, 150, 171, 31))
        self.kwplainTextEdit.setObjectName("kwplainTextEdit")
        self.keywords_label = QtWidgets.QLabel(self.centralwidget)
        self.keywords_label.setGeometry(QtCore.QRect(40, 160, 101, 19))
        self.keywords_label.setObjectName("keywords_label")
        self.date_checkBox = QtWidgets.QRadioButton(self.centralwidget)
        self.date_checkBox.setGeometry(QtCore.QRect(150, 230, 121, 25))
        self.date_checkBox.setObjectName("date_checkBox")
        self.user_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.user_checkBox.setGeometry(QtCore.QRect(150, 270, 92, 25))
        self.user_checkBox.setObjectName("user_checkBox")
        self.hashtag_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.hashtag_checkBox.setGeometry(QtCore.QRect(150, 320, 92, 25))
        self.hashtag_checkBox.setObjectName("hashtag_checkBox")
        self.noRT_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.noRT_checkBox.setGeometry(QtCore.QRect(150, 350, 121, 25))
        self.noRT_checkBox.setObjectName("noRT_checkBox")
        self.dateEdit_start = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_start.setGeometry(QtCore.QRect(380, 190, 110, 28))
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.dateEdit_start.setDisplayFormat("dd/MM/yyyy")
        self.dateEdit_end = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_end.setGeometry(QtCore.QRect(560, 190, 110, 28))
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.dateEdit_end.setDisplayFormat("dd/MM/yyyy")
        self.dateinitial_label = QtWidgets.QLabel(self.centralwidget)
        self.dateinitial_label.setGeometry(QtCore.QRect(330, 190, 67, 19))
        self.dateinitial_label.setObjectName("dateinitial_label")
        self.dateend_label = QtWidgets.QLabel(self.centralwidget)
        self.dateend_label.setGeometry(QtCore.QRect(510, 190, 67, 19))
        self.dateend_label.setObjectName("dateend_label")
        self.dateEdit_exact = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_exact.setGeometry(QtCore.QRect(380, 230, 110, 28))
        self.dateEdit_exact.setObjectName("dateEdit_exact")
        self.dateEdit_exact.setDisplayFormat("dd/MM/yyyy")
        self.user_plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.user_plainTextEdit.setGeometry(QtCore.QRect(380, 270, 104, 31))
        self.user_plainTextEdit.setObjectName("user_plainTextEdit")
        self.hashtag_plainTextEdit = QtWidgets.QPlainTextEdit(
            self.centralwidget)
        self.hashtag_plainTextEdit.setGeometry(QtCore.QRect(380, 310, 104, 31))
        self.hashtag_plainTextEdit.setObjectName("hashtag_plainTextEdit")
        self.stats_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stats_pushButton.setGeometry(QtCore.QRect(360, 50, 151, 27))
        self.stats_pushButton.setObjectName("stats_pushButton")
        self.results_TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.results_TextBrowser.setGeometry(QtCore.QRect(40, 490, 671, 271))
        self.results_TextBrowser.setText("")
        self.results_TextBrowser.setObjectName("results_label")

        # self.horizontal_layout.addWidget(self.results_TextBrowser)

        # self.results_TextBrowser.setSizePolicy(
        #    QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(350, 400, 211, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.filter_label = QtWidgets.QLabel(self.centralwidget)
        self.filter_label.setGeometry(QtCore.QRect(260, 110, 201, 19))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.filter_label.setFont(font)
        self.filter_label.setObjectName("filter_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_pushButton.setText(_translate("MainWindow", "Buscar"))
        self.collections_label.setText(_translate("MainWindow", "Colecciones"))
        self.daterange_checkBox.setText(
            _translate("MainWindow", "Rango de fechas"))
        self.keywords_label.setText(_translate("MainWindow", "Palabras clave"))
        self.date_checkBox.setText(_translate("MainWindow", "Fecha exacta"))
        self.user_checkBox.setText(_translate("MainWindow", "Usuario"))
        self.hashtag_checkBox.setText(_translate("MainWindow", "Hashtag"))
        self.noRT_checkBox.setText(_translate("MainWindow", "Descartar RT"))
        self.dateinitial_label.setText(_translate("MainWindow", "Inicial"))
        self.dateend_label.setText(_translate("MainWindow", "Final"))
        self.stats_pushButton.setText(_translate(
            "MainWindow", "Obtener estadísticas"))
        self.status_label.setText(_translate("MainWindow", "En espera"))
        self.filter_label.setText(_translate(
            "MainWindow", "Filtrado de Tweets"))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._connect()
        self._update_col_ComboBox()

        self.ui.stats_pushButton.clicked.connect(self._get_collection_stats)
        self.ui.search_pushButton.clicked.connect(self._filter_tweets)

    def _connect(self):
        self.db_manager = MDBMan.DBManager('twitter_downloads')

    '''
    Update combobox contents with the new lists of collections from database
    '''

    def _update_col_ComboBox(self):

        # Read list of collections existents in the database
        col_list = self.db_manager.show_collections_list()

        # Remove all contents of combobox
        self.ui.collection_comboBox.clear()

        # Fill combobox with the new list of collections
        self.ui.collection_comboBox.addItems(col_list)

    '''
    Get all statistics of a collection, and show it in the interface
    '''

    def _get_collection_stats(self):

        # Read collection name from the interface
        collection = self.ui.collection_comboBox.currentText()

        # Get collection stats tool
        col_manager = self.db_manager.get_collection_manager(collection)
        stats = col_manager.get_stats()

        # Get string with all stats results
        stats_str = stats.show_all_stats()

        # Show text in the interface
        self.ui.results_TextBrowser.setText(stats_str)

    '''
    Create a new collection and prepare it for send queries
    '''

    def __update_query_collection(self, collection_name: str, docs):

        # Load data in a new temporary collection
        col_manager = self.db_manager.load_collection_from_bson(
            docs, collection_name)

        # If the collection has not a text index, create it
        if not col_manager.check_text_index("full_text"):
            col_manager.create_text_index("full_text")

        # Get query tool from the new collection
        query_col = col_manager.get_query()

        return query_col

    '''
    Remove all temporary collections from the database
    '''

    def __remove_temporary_collections(self, collection_name: str):
        collection_list = self.db_manager.show_collections_list()

        col_name = f"{collection_name}_keywords"
        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

        col_name = f"{collection_name}_daterange"
        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

        col_name = f"{collection_name}_date"
        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

        col_name = f"{collection_name}_user"
        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

        col_name = f"{collection_name}_hashtag"
        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

        col_name = f"{collection_name}_nort"

        if col_name in collection_list:
            self.db_manager.remove_collection(col_name)

    '''
    Filter a subset of tweets, stored in a MongoDB database, using a set of filters with different cryteria
    '''

    def _filter_tweets(self):

        # Read collection name
        collection = self.ui.collection_comboBox.currentText()

        # Access to collection
        col_manager = self.db_manager.get_collection_manager(collection)

        # If the collection has not a text index, create a new text index in the full_text tweet field
        if not col_manager.check_text_index("full_text"):
            col_manager.create_text_index("full_text")

        # Read keywords to filter from the interface (obligatory)
        keywords = self.ui.kwplainTextEdit.toPlainText()

        # Get querytool for this collection
        query_col = col_manager.get_query()

        # Filter documents using the keywords
        docs = query_col.find_docs_by_keywords(keywords)

        # Set the destination collection's name
        collection_name = f"{collection}_filtered"

        # If the query results any document, store them in a temporary collection
        if docs.count() > 0:
            col_name = f"{collection_name}_keywords"
            query_col = self.__update_query_collection(col_name, docs)

        # If the last query got any document, and the user enable daterange filter, filter again over the temporary collection
        if docs.count() > 0 and self.ui.daterange_checkBox.isChecked():

            # Read start and end date from the interface
            start_date = self.ui.dateEdit_start.date().toString("dd-MM-yyyy")
            end_date = self.ui.dateEdit_end.date().toString("dd-MM-yyyy")

            # Filter documents by date range from the temporary collection, stored in the database
            docs = query_col.find_docs_by_date_range(start_date, end_date)

            # If the query get any results, store them in a new temporary collection
            col_name = f"{collection_name}_daterange"
            if docs.count() > 0:
                query_col = self.__update_query_collection(
                    col_name, docs)

        # If the user enable exact date filter instead daterange filter, filter again over the temporary collection
        elif docs.count() > 0 and self.ui.date_checkBox.isChecked():

            # Read date from the interface
            date = self.ui.dateEdit_exact.date().toString("dd-MM-yyyy")

            # Filter documents by exact date from the temporary collection, stored in the database
            docs = query_col.find_docs_by_date(date)

            # If the query get any results, store them in a new temporary collection
            col_name = f"{collection_name}_date"
            if docs.count() > 0:
                query_col = self.__update_query_collection(
                    col_name, docs)

        # If the last query got any results, and user enable filter by user, filter again over the temporary collection
        if docs.count() > 0 and self.ui.user_checkBox.isChecked():

            # Read username to filter from the interface
            user = self.ui.user_plainTextEdit.toPlainText()

            # Filter documents using username
            docs = query_col.find_docs_by_user(user)

            # if the query results any document, store them in a new temporary collection
            col_name = f"{collection_name}_user"
            if docs.count() > 0:
                query_col = self.__update_query_collection(
                    col_name, docs)

        # If the last query got any results, and the user enable filter by hashtag, filter again over the temporary collection
        if docs.count() > 0 and self.ui.hashtag_checkBox.isChecked():

            # Read hashtag to filter from the interface
            hashtag = self.ui.hashtag_plainTextEdit.toPlainText()

            # Filter documents by this hashtag
            docs = query_col.find_docs_by_hashtag(hashtag)

            # If the query got any result, store them in a new temporary collection
            col_name = f"{collection_name}_hashtag"
            if docs.count() > 0:
                query_col = self.__update_query_collection(
                    col_name, docs)

        # If the last query got any results, and user enable filter by noRT, filter again over the temporary collection
        if docs.count() > 0 and self.ui.noRT_checkBox.isChecked():

            # Filter documents from temporary collection, discarting retweets
            docs = query_col.find_docs_no_retweet()

            # if the query get any results, store them in a new temporary collection
            col_name = f"{collection_name}_nort"
            if docs.count() > 0:
                query_col = self.__update_query_collection(
                    col_name, docs)

        # If the last query got any results, remove all temporary collection, and store the latest results in a new collection
        if docs.count() > 0:

            # Final collection name
            final_collection_name = f"{collection}_filtered"

            # Load documents in the final collection
            colm = self.db_manager.load_collection_from_bson(
                docs, final_collection_name)

            # Remove all temporary collections
            self.__remove_temporary_collections(collection)

            print(self.db_manager.show_collections_list())

            # Update combobox with the new collections
            self._update_col_ComboBox()

            # Show sucess status in the interface
            self.ui.status_label.setText("Success")

        # If the last query got zero results, remove all temporary collections, and show message "No results" in the interface
        else:
            self.__remove_temporary_collections(collection)
            self.ui.status_label.setText("No results")


if __name__ == "__main__":
    app = QtWidgets.QApplication(["Twitter Queries"])

    mainWindow = QtWidgets.QMainWindow()
    window = MainWindow()
    window.setWindowTitle("Twitter Queries")
    window.show()

    sys.exit(app.exec())
