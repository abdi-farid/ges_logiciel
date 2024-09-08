import os
import sys
import src._icon_rc

from PyQt6.QtWidgets import QApplication

from src._1_module_consommation.controllers._1_conso_gaz_controller import ConsommationGazController
from src.configuration.controllers.app_electrique_controller import AppareilElectriqueController
from src.configuration.controllers.app_gaz_controller import AppareilGazController
from src.ui_interface import *

# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## Controllers
        self.conf_app_elec_controller = None
        self.conf_app_gaz_controller = None
        self.module_1_conso_gaz_controller = None

        # Use this if you only have one json file named "style.json" inside the root directory, "json" directory or "jsonstyles" folder.
        # loadJsonStyle(self, self.ui) 

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })

        self.ui.stackedWidget.setCurrentWidget(self.ui._1_page_home)

        self.ui.action_conf_elec.triggered.connect(lambda: self.load_conf_electrique())
        self.ui.action_conf_gaz.triggered.connect(lambda: self.load_conf_gaz())

        self.ui.action_conso_elec.triggered.connect(lambda: self.load_consommation_elec())
        self.ui.action_conso_gaz.triggered.connect(lambda: self.load_consommation_gaz())

        self.show()

        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

    def load_conf_electrique(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_config_electrique)

        if self.conf_app_elec_controller is None:  # Ne recréez pas le contrôleur s'il existe déjà
            self.conf_app_elec_controller = AppareilElectriqueController(self)

    def load_conf_gaz(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_config_gaz)

        if self.conf_app_gaz_controller is None:  # Ne recréez pas le contrôleur s'il existe déjà
            self.conf_app_gaz_controller = AppareilGazController(self)

    def load_consommation_elec(self):
        print('load module 1 :  consommation elec')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1_consommation_elec)

        # if self.conf_app_gaz_controller is None:  # Ne recréez pas le contrôleur s'il existe déjà
        #    self.conf_app_gaz_controller = AppareilGazController(self)

    def load_consommation_gaz(self):
        print('load module 1 :  consommation Gaz')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1_consommation_gaz)

        if self.module_1_conso_gaz_controller is None:  # Ne recréez pas le contrôleur s'il existe déjà
            self.module_1_conso_gaz_controller = ConsommationGazController(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
