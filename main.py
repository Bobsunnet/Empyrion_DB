import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import db_interface as db
import TableView
from FieldChecker import FieldChecker

ITEM_HEADERS = ['Item Name', 'Place','Avg Price', 'Buy Price', 'Buy Amount', 'Sell Price', 'Sell Amount']
POI_HEADERS = []
RESOURCE_HEADERS = ['Resource', 'Place']

VALIDATOR_DIGITS = QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9]+'))


def success_log_deco(func):
    def wrapper(*args, **kwargs):
        operation_status = func(*args, **kwargs)
        if operation_status:
            print(operation_status)
        else:
            print('trying to drow error_box')
            #обращаемся к экземпляру окна MainWindow() и вызываем у него метод отображения сообщения
            window.draw_message_box('ERROR', 'Some error occurred. Please look the console log')
        return operation_status

    return wrapper


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Empyrion Data Base')
        self.setGeometry(1000, 200, 600, 280)

        self.data_cache = db.DataCache()

        self.global_widgets_setup()
        self.completer_setup()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tab_widget.setMovable(True)
        widgets_list = [
            (self.window_add_poi, self.window_add_poi.windowTitle()),
            (self.window_add_place, self.window_add_place.windowTitle()),
            (self.window_add_new_item, self.window_add_new_item.windowTitle()),
            (self.window_add_resource, self.window_add_resource.windowTitle()),
            (self.window_add_market_item, self.window_add_market_item.windowTitle()),
            (self.window_search, self.window_search.windowTitle())
        ]
        for widget_data in widgets_list:
            self.tab_widget.addTab(widget_data[0], widget_data[1])
        self.tab_widget.currentChanged.connect(self.tab_changed)

        self.fill_comboboxes()

        # ____________________________OBOSOLETE BUTTONS. NEED REMADE__________________________________

        self.btn_1 = QtWidgets.QPushButton('1')

        self.btn_2 = QtWidgets.QPushButton('2')

        self.btn_3 = QtWidgets.QPushButton('3')

        self.btn_4 = QtWidgets.QPushButton('4')

        self.btn_5 = QtWidgets.QPushButton('5')

        # _________________________________LAYOUTS_______________________________________
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.btn_1)
        top_layout.addWidget(self.btn_2)
        top_layout.addWidget(self.btn_3)
        top_layout.addWidget(self.btn_4)
        top_layout.addWidget(self.btn_5)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tab_widget)

        top_layout_widget = QtWidgets.QWidget()
        top_layout_widget.setLayout(main_layout)

        self.setCentralWidget(top_layout_widget)

    def completer_setup(self):
        self.item_completer = QtWidgets.QCompleter(self.data_cache.item_dict.keys(), self)
        self.item_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.lnedit_item.setCompleter(self.item_completer)
        self.lnedit_item_market.setCompleter(self.item_completer)
        self.lnedit_search_item.setCompleter(self.item_completer)

        self.poi_completer = QtWidgets.QCompleter(self.data_cache.poi_dict.keys(), self)
        self.poi_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.lnedit_poi.setCompleter(self.poi_completer)
        self.lnedit_poi_item.setCompleter(self.poi_completer)
        self.lnedit_search_poi.setCompleter(self.poi_completer)

        self.system_completer = QtWidgets.QCompleter(self.data_cache.system_dict.keys(), self)
        self.system_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.lnedit_system.setCompleter(self.system_completer)

        self.place_completer = QtWidgets.QCompleter(self.data_cache.place_dict.keys(), self)
        self.place_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.lnedit_place.setCompleter(self.place_completer)
        self.lnedit_place_poi.setCompleter(self.place_completer)
        self.lnedit_place_res.setCompleter(self.place_completer)

    def global_widgets_setup(self):
        # ____________________________________________ADD_PLACE______________________________________
        self.window_add_place = QtWidgets.QWidget()
        self.window_add_place.setWindowTitle('Add new place')

        self.label_system = QtWidgets.QLabel('System')
        self.lnedit_system = QtWidgets.QLineEdit()

        self.label_place = QtWidgets.QLabel('Place')
        self.lnedit_place = QtWidgets.QLineEdit()

        self.label_star_class = QtWidgets.QLabel('Star class')
        self.lnedit_star_class = QtWidgets.QLineEdit()

        self.btn_add_place = QtWidgets.QPushButton('Add place')
        self.btn_add_place.clicked.connect(self.btn_add_place_clicked)

        add_place_main_layout = QtWidgets.QVBoxLayout()
        #
        add_place_first_layout = QtWidgets.QHBoxLayout()
        add_place_first_layout.addWidget(self.label_system)
        add_place_first_layout.addWidget(self.lnedit_system)

        add_place_second_layout = QtWidgets.QHBoxLayout()
        add_place_second_layout.addWidget(self.label_place)
        add_place_second_layout.addWidget(self.lnedit_place)
        #
        add_place_third_layout = QtWidgets.QHBoxLayout()
        add_place_third_layout.addWidget(self.label_star_class)
        add_place_third_layout.addWidget(self.lnedit_star_class)
        #
        add_place_main_layout.addLayout(add_place_first_layout)
        add_place_main_layout.addLayout(add_place_second_layout)
        add_place_main_layout.addLayout(add_place_third_layout)
        #
        add_place_main_layout.addWidget(self.btn_add_place)
        #
        self.window_add_place.setLayout(add_place_main_layout)

        # ____________________________________________ADD_POI______________________________________
        self.window_add_poi = QtWidgets.QWidget()
        self.window_add_poi.setWindowTitle('Add new POI')

        self.checkbox_new_poi = QtWidgets.QCheckBox('POI Location')
        self.checkbox_new_poi.clicked.connect(self.checkbox_place_input_clicked)

        self.label_faction = QtWidgets.QLabel('Chose Faction')
        self.combox_faction = QtWidgets.QComboBox()
        self.combox_faction.setDisabled(True)

        self.label_poi = QtWidgets.QLabel('POI Name')
        self.lnedit_poi = QtWidgets.QLineEdit()

        self.label_place_poi = QtWidgets.QLabel('Chose place')
        self.lnedit_place_poi = QtWidgets.QLineEdit()

        self.btn_add_poi = QtWidgets.QPushButton('Add POI')
        self.btn_add_poi.clicked.connect(self.btn_add_poi_clicked)

        add_poi_main_layout = QtWidgets.QVBoxLayout()
        #
        add_poi_first_layout = QtWidgets.QHBoxLayout()
        add_poi_first_layout.addWidget(self.label_place_poi)
        add_poi_first_layout.addWidget(self.lnedit_place_poi)
        add_poi_first_layout.addWidget(self.checkbox_new_poi)

        add_poi_second_layout = QtWidgets.QHBoxLayout()
        add_poi_second_layout.addWidget(self.label_faction)
        add_poi_second_layout.addWidget(self.combox_faction)

        add_poi_third_layout = QtWidgets.QHBoxLayout()
        add_poi_third_layout.addWidget(self.label_poi)
        add_poi_third_layout.addWidget(self.lnedit_poi)

        add_poi_main_layout.addLayout(add_poi_first_layout)
        add_poi_main_layout.addLayout(add_poi_second_layout)
        add_poi_main_layout.addLayout(add_poi_third_layout)
        add_poi_main_layout.addWidget(self.btn_add_poi)

        self.window_add_poi.setLayout(add_poi_main_layout)

        # ____________________________________________ADD_RESOURCE______________________________________
        self.window_add_resource = QtWidgets.QWidget()
        self.window_add_resource.setWindowTitle('Add resource')

        self.label_resource = QtWidgets.QLabel('Resource')
        self.combox_resource = QtWidgets.QComboBox()

        self.label_place_res = QtWidgets.QLabel('Chose place')
        self.lnedit_place_res = QtWidgets.QLineEdit()

        self.btn_add_resource = QtWidgets.QPushButton('Add Resource')
        self.btn_add_resource.clicked.connect(self.btn_add_resource_location_clicked)

        add_resource_main_layout = QtWidgets.QVBoxLayout()

        add_resource_first_layout = QtWidgets.QHBoxLayout()
        add_resource_first_layout.addWidget(self.label_place_res)
        add_resource_first_layout.addWidget(self.lnedit_place_res)

        add_resource_second_layout = QtWidgets.QHBoxLayout()
        add_resource_second_layout.addWidget(self.label_resource)
        add_resource_second_layout.addWidget(self.combox_resource)

        add_resource_main_layout.addLayout(add_resource_first_layout)
        add_resource_main_layout.addLayout(add_resource_second_layout)
        add_resource_main_layout.addWidget(self.btn_add_resource)

        self.window_add_resource.setLayout(add_resource_main_layout)

        # ____________________________________________ADD_NEW_ITEM________________________________________
        self.window_add_new_item = QtWidgets.QWidget()
        self.window_add_new_item.setWindowTitle('Add New Item')

        self.label_item_name = QtWidgets.QLabel('Item Name')
        self.lnedit_item = QtWidgets.QLineEdit()

        self.label_avg_price = QtWidgets.QLabel('Avg Price')
        self.lnedit_avg_price = QtWidgets.QLineEdit()
        self.lnedit_avg_price.setValidator(VALIDATOR_DIGITS)

        self.btn_add_item = QtWidgets.QPushButton('Add new item')
        self.btn_add_item.clicked.connect(self.btn_add_new_item_clicked)

        new_item_first_layout = QtWidgets.QHBoxLayout()
        new_item_first_layout.addWidget(self.label_item_name)
        new_item_first_layout.addWidget(self.lnedit_item)

        new_item_second_layout = QtWidgets.QHBoxLayout()
        new_item_second_layout.addWidget(self.label_avg_price)
        new_item_second_layout.addWidget(self.lnedit_avg_price)

        new_item_main_layout = QtWidgets.QVBoxLayout()
        new_item_main_layout.addLayout(new_item_first_layout)
        new_item_main_layout.addLayout(new_item_second_layout)
        new_item_main_layout.addWidget(self.btn_add_item)

        self.window_add_new_item.setLayout(new_item_main_layout)

        # __________________________________________ADD_MARKET_ITEM________________________________________
        self.window_add_market_item = QtWidgets.QWidget()
        self.window_add_market_item.setWindowTitle('Add Market Item')

        self.label_poi_item = QtWidgets.QLabel('Chose Poi')
        self.lnedit_poi_item = QtWidgets.QLineEdit()

        self.label_item_market = QtWidgets.QLabel('Item Name')
        self.lnedit_item_market = QtWidgets.QLineEdit()

        self.label_buy_price = QtWidgets.QLabel('Buy Price')
        self.lnedit_buy_price = QtWidgets.QLineEdit()
        self.lnedit_buy_price.setValidator(VALIDATOR_DIGITS)

        self.label_buy_amount = QtWidgets.QLabel('Buy Amount')
        self.lnedit_buy_amount = QtWidgets.QLineEdit()
        self.lnedit_buy_amount.setValidator(VALIDATOR_DIGITS)

        self.label_sell_price = QtWidgets.QLabel('Sell Price')
        self.lnedit_sell_price = QtWidgets.QLineEdit()
        self.lnedit_sell_price.setValidator(VALIDATOR_DIGITS)

        self.label_sell_amount = QtWidgets.QLabel('Sell Amount')
        self.lnedit_sell_amount = QtWidgets.QLineEdit()
        self.lnedit_sell_amount.setValidator(VALIDATOR_DIGITS)

        self.btn_add_market_item = QtWidgets.QPushButton('Add_market_item')
        self.btn_add_market_item.clicked.connect(self.btn_new_market_item_clicked)

        market_item_first_layout = QtWidgets.QHBoxLayout()
        market_item_first_layout.addWidget(self.label_poi_item)
        market_item_first_layout.addWidget(self.lnedit_poi_item)

        market_item_second_layout = QtWidgets.QHBoxLayout()
        market_item_second_layout.addWidget(self.label_item_market)
        market_item_second_layout.addWidget(self.lnedit_item_market)

        market_item_third_layout = QtWidgets.QHBoxLayout()
        market_item_third_layout.addWidget(self.label_buy_price)
        market_item_third_layout.addWidget(self.lnedit_buy_price)
        market_item_third_layout.addWidget(self.label_buy_amount)
        market_item_third_layout.addWidget(self.lnedit_buy_amount)

        market_item_fourth_layout = QtWidgets.QHBoxLayout()
        market_item_fourth_layout.addWidget(self.label_sell_price)
        market_item_fourth_layout.addWidget(self.lnedit_sell_price)
        market_item_fourth_layout.addWidget(self.label_sell_amount)
        market_item_fourth_layout.addWidget(self.lnedit_sell_amount)

        market_item_main_layout = QtWidgets.QVBoxLayout()
        market_item_main_layout.addLayout(market_item_first_layout)
        market_item_main_layout.addLayout(market_item_second_layout)
        market_item_main_layout.addLayout(market_item_third_layout)
        market_item_main_layout.addLayout(market_item_fourth_layout)
        market_item_main_layout.addWidget(self.btn_add_market_item)

        self.window_add_market_item.setLayout(market_item_main_layout)

        # __________________________________________SEARCH_WIDGET__________________________________________
        self.window_search = QtWidgets.QWidget()
        self.window_search.setWindowTitle('Search All')

        self.lbl_search_res = QtWidgets.QLabel('Chose Resource')
        self.combox_search_resource = QtWidgets.QComboBox()
        self.btn_search_resource_single = QtWidgets.QPushButton('Search')
        self.btn_search_resource_single.clicked.connect(self.btn_search_resource_clicked)
        self.btn_search_resource_all = QtWidgets.QPushButton('Show All')
        self.btn_search_resource_all.clicked.connect(self.btn_search_resource_all_clicked)

        self.lbl_search_poi = QtWidgets.QLabel("Chose POI")
        self.lnedit_search_poi = QtWidgets.QLineEdit()
        self.lnedit_search_poi.setPlaceholderText('Type POI name')
        self.btn_search_poi_single = QtWidgets.QPushButton('Search')
        self.btn_search_poi_single.clicked.connect(self.btn_search_poi_clicked)
        self.btn_search_poi_all = QtWidgets.QPushButton('Show All')
        self.btn_search_poi_all.clicked.connect(self.btn_search_poi_all_clicked)

        self.lbl_search_item = QtWidgets.QLabel("Chose Item")
        self.lnedit_search_item = QtWidgets.QLineEdit()
        self.lnedit_search_item.setPlaceholderText('Type item name')
        self.btn_search_item_single = QtWidgets.QPushButton('Search')
        self.btn_search_item_single.clicked.connect(self.btn_search_item_clicked)
        self.btn_search_item_all = QtWidgets.QPushButton('Show All')
        self.btn_search_item_all.clicked.connect(self.btn_search_item_all_clicked)


        search_widget_first_layout = QtWidgets.QHBoxLayout()
        search_widget_first_layout.addWidget(self.lbl_search_res)
        search_widget_first_layout.addWidget(self.combox_search_resource)
        search_widget_first_layout.addWidget(self.btn_search_resource_all)
        search_widget_first_layout.addWidget(self.btn_search_resource_single)

        search_widget_second_layout = QtWidgets.QHBoxLayout()
        search_widget_second_layout.addWidget(self.lbl_search_poi)
        search_widget_second_layout.addWidget(self.lnedit_search_poi)
        search_widget_second_layout.addWidget(self.btn_search_poi_all)
        search_widget_second_layout.addWidget(self.btn_search_poi_single)

        search_widget_third_layout = QtWidgets.QHBoxLayout()
        search_widget_third_layout.addWidget(self.lbl_search_item)
        search_widget_third_layout.addWidget(self.lnedit_search_item)
        search_widget_third_layout.addWidget(self.btn_search_item_all)
        search_widget_third_layout.addWidget(self.btn_search_item_single)

        search_widget_main_layout = QtWidgets.QVBoxLayout()
        search_widget_main_layout.addLayout(search_widget_first_layout)
        search_widget_main_layout.addLayout(search_widget_second_layout)
        search_widget_main_layout.addLayout(search_widget_third_layout)

        self.window_search.setLayout(search_widget_main_layout)

    def fill_comboboxes(self):
        # inserting data from db_cash to comboboxes
        resource_list = sorted(tuple(self.data_cache.resource_dict.keys()))
        faction_list = sorted(tuple(self.data_cache.faction_dict.keys()))
        self.combox_resource.addItems(resource_list)
        self.combox_faction.addItems(faction_list)
        self.combox_search_resource.addItems(resource_list)

    def refresh_data_cache(self):
        # TODO: needs to be reworked
        self.data_cache.update_all_dicts()

    def checkbox_place_input_clicked(self):
        if self.checkbox_new_poi.isChecked():
            self.lnedit_place_poi.setDisabled(True)
            self.checkbox_new_poi.setText('New POI')
            self.combox_faction.setDisabled(False)
        else:
            self.lnedit_place_poi.setDisabled(False)
            self.checkbox_new_poi.setText('POI Location')
            self.combox_faction.setDisabled(True)

    # __________________________________ <EVENTS> ___________________________________________
    def tab_changed(self):
        pass

    def btn_search_resource_clicked(self):
        self._load_resource_single()

    def btn_search_resource_all_clicked(self):
        self._load_resource_all()

    def btn_search_poi_clicked(self):
        self._load_poi_single()

    def btn_search_poi_all_clicked(self):
        self._load_poi_all()

    def btn_search_item_clicked(self):
        self._load_item_single()

    def btn_search_item_all_clicked(self):
        self._load_item_all()

    def btn_add_poi_clicked(self):
        if self.checkbox_new_poi.isChecked():
            self.add_new_poi()
            self.data_cache.update_poi_dict()
            self.completer_setup()
        else:
            self.add_poi_location()

    def btn_add_new_item_clicked(self):
        self.add_new_item()
        self.data_cache.update_item_dict()
        self.completer_setup()

    def btn_add_place_clicked(self):
        self.add_new_place()
        self.data_cache.update_place_dict()
        self.completer_setup()

    def btn_add_resource_location_clicked(self):
        self.add_resource_location()

    def btn_new_market_item_clicked(self):
        self.add_market_item()

    # ____________________________________ <SLOTS> _____________________________________________
    def draw_result_table(self, table_data:list, table_headers):
        self.table_window = TableView.TableWindow(table_data, table_headers)
        self.table_window.show()

    def draw_message_box(self, title, message):
        self.message = QtWidgets.QMessageBox()
        self.message.setWindowTitle(title)
        self.message.setText(message)
        self.message.show()

    def draw_message_empty_result(self):
        self.message = QtWidgets.QMessageBox()
        self.message.setWindowTitle('Not Found')
        self.message.setText('No Result on your query =(')
        self.message.show()

    # _____________________________________ <LOGIC> _____________________________________________

    # _____________________________________ ADD_DATA ___________________________________________
    @ success_log_deco
    def add_new_item(self):
        name = self.lnedit_item.text()
        price = int(self.lnedit_avg_price.text())
        return db.add_item(name, price)

    @success_log_deco
    def add_new_place(self):
        system_input = self.lnedit_system.text().lower()
        place_input = self.lnedit_place.text().lower()
        star_class = self.lnedit_star_class.text().upper()

        system_id = self.data_cache.system_dict.get(system_input)
        if not system_id:
            self._add_new_system(system_input, star_class)
            self.data_cache.update_system_dict()
        system_id = self.data_cache.system_dict.get(system_input)

        return db.add_place(place_input, system_id)

    @success_log_deco
    def _add_new_system(self,sys_name, star_cls):
        return db.add_star_system(sys_name, star_cls)

    @success_log_deco
    def add_new_poi(self):
        poi_name = self.lnedit_poi.text()
        faction = self.combox_faction.currentText()
        return db.add_poi(poi_name, self.data_cache.faction_dict.get(faction))

    @success_log_deco
    def add_poi_location(self):
        poi_name = self.lnedit_poi.text()
        place_name = self.lnedit_place_poi.text()
        return db.add_poi_location(self.data_cache.poi_dict.get(poi_name), self.data_cache.place_dict.get(place_name))

    @success_log_deco
    def add_resource_location(self):
        place_id = self.data_cache.place_dict.get(self.lnedit_place_res.text())
        res_id = self.data_cache.resource_dict.get(self.combox_resource.currentText())
        return db.add_resource_location(res_id, place_id)

    @success_log_deco
    def add_market_item(self):
        poi_id = self.data_cache.poi_dict.get(self.lnedit_poi_item.text())
        item_id = self.data_cache.item_dict.get(self.lnedit_item_market.text())

        buy_price = self._string_converter(self.lnedit_buy_price.text())
        buy_amount = self._string_converter(self.lnedit_buy_amount.text())
        sell_price = self._string_converter(self.lnedit_sell_price.text())
        sell_amount = self._string_converter(self.lnedit_sell_amount.text())

        return db.add_item_market(poi_id, item_id, buy_price, buy_amount, sell_price, sell_amount)

    # _______________________________________ SEARCHING DATA ___________________________________

    def _load_resource_single(self):
        #загружаем данные из БД по тексту в комбобоксе.
        res_name: str = self.combox_search_resource.currentText()
        self.search_resource(self.load_resource_data(res_name))

            # TODO попробовать отрефакторить два метода в один
    def _load_resource_all(self):
        # загружаем данные из БД
        self.search_resource(self.load_resource_data())

    def search_resource(self, res_data:list):
        # конвертируем данные в таблицу и рисуем результат
        res_table: list = self.create_resource_table(res_data)
        if res_table:
            self.draw_result_table(res_table, RESOURCE_HEADERS)
        else:
            self.draw_message_empty_result()

    def _load_item_single(self):
        item_name = self.lnedit_search_item.text().lower()
        self.search_item(self.load_item_data(item_name))

    def _load_item_all(self):
        self.search_item(self.load_item_data())

    def search_item(self, item_data: list):
        item_table: list = self.create_item_table(item_data)
        if item_table:
            self.draw_result_table(item_table, ITEM_HEADERS)
        else:
            self.draw_message_empty_result()

    def _load_poi_single(self):
        poi_name: str = self.lnedit_search_poi.text()
        self.search_poi(self.load_poi_data(poi_name))

    def _load_poi_all(self):
        self.search_poi(self.load_poi_data())


    def search_poi(self, poi_data: list):
        poi_table: list = self.create_poi_table(poi_data)
        if poi_table:
            self.draw_result_table(poi_table, POI_HEADERS)
        else:
            self.draw_message_empty_result()

    # ___________________________________ LOADING DATA (temporary) _____________________________
    @staticmethod
    def load_item_data(item_name=''):
        # TODO 1. возможно использовать датакеш для хранения результатов поиска
        # TODO 2. попробовать отрефакторить
        ''':return list of resource data object'''
        item_data = db.ItemLoader()
        item_data.load_item(item_name)
        return item_data.get_data()

    @staticmethod
    def load_resource_data(res_name=''):
        # TODO 1. возможно использовать датакеш для хранения результатов поиска
        # TODO 2. попробовать отрефакторить
        ''':return list of resource data object'''
        res_data = db.ResourceLoader()
        res_data.load_resource(res_name)
        return res_data.get_data()

    @staticmethod
    def load_poi_data(poi_name=''):
        poi_data = db.PoiLoader()
        poi_data.load_poi(poi_name)
        return poi_data.get_data()

    # _____________________________ CREATING TABLES(temporary) ________________________
    @staticmethod
    def create_item_table(item_data):
        item_table = db.ItemTable(item_data)
        return item_table.make_item_table()

    @staticmethod
    def create_resource_table(res_data: list):
        res_table = db.ResourceTable(res_data)
        return res_table.make_resource_table()

    @staticmethod
    def create_poi_table(poi_data: list):
        print('creating table started')
        poi_table = db.PoiTable(poi_data)
        return poi_table.make_poi_table()

    # _____________________________________ MISC ______________________________________

    @staticmethod
    def _string_converter(value):
        # checks if string is empty and return int('0')
        return int(value) if value else 0


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
