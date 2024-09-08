from PyQt6 import QtWidgets

from core.databse import Database
from src._1_module_consommation.models._1_conso_gaz import ConsommationGaz
from src._1_module_consommation.tableModels._1_conso_gaz_table_model import ConsommationGazTableModel

from src.configuration.tableModels.app_gaz_table_model import TABLE_NAME as APP_GAZ_TABLE_NAME


class ConsommationGazController:
    def __init__(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self.ui = main_window.ui

        self.table_model = ConsommationGazTableModel()
        self.ui.tableView_conso_gaz.setModel(self.table_model)

        # Masquer la première colonne (ID)
        self.ui.tableView_conso_gaz.hideColumn(0)

        self.calculate_loading_items()

        for element in self.table_model.appareils:
            print(element)
            self.ui.appareilGazComboBox.addItem(f'{element[1]} ({element[2]} W)', element)
            print('current data combo :: ', self.ui.appareilGazComboBox.currentData())

        self.ui.add_conso_gaz.clicked.connect(lambda: self.add_item())
        self.ui.edit_conso_gaz.clicked.connect(lambda: self.update_item())
        self.ui.clear_conso_gaz.clicked.connect(lambda: self.clear_input())
        self.ui.del_conso_gaz.clicked.connect(lambda: self.delete_item())
        self.ui.tableView_conso_gaz.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def calculate_consommation(self):
        database = Database()
        sum = 0
        for element in self.table_model.consommations:
            appareil = database.get_record_by_id(APP_GAZ_TABLE_NAME, element[1])
            print('appareil trouvé est : ')
            print(element)
            # indice deux nbr appareil, indice 3 nbr heure utilisation
            sum += element[2] * appareil['puissance'] * element[3]

        self.ui.lcdConsommationGaz.display(sum)

    def add_item(self):
        consommation = self.get_inputs()
        if consommation is not None and self.validate_app_input(consommation):
            self.table_model.add_consommation(consommation)
            self.clear_input()
            self.calculate_consommation()

    def update_item(self):
        id_ = self.get_selected_id()

        if id_ is None:
            QtWidgets.QMessageBox.warning(self.main_window, "Attention",
                                          "Veuillez sélectionner un appareil à modifier.")
            return

        appareil = self.get_inputs()

        # Mise à jour dans la base de données avec l'ID récupéré
        self.table_model.update_consommation(id_, appareil)

        self.clear_input()
        self.ui.add_conso_gaz.setEnabled(True)
        self.calculate_consommation()

    def on_selection_changed(self):
        id_ = self.get_selected_id()

        if id_ is not None:
            # Chercher l'appareil dans la liste en fonction de l'ID
            consommation = next((item for item in self.table_model.consommations if item[0] == id_), None)

            if consommation:
                appareil = next((item for item in self.table_model.appareils if item[0] == consommation[1]), None)
                print('appareil : ', appareil)
                # Mettre à jour les champs de saisie avec les données de l'appareil sélectionné
                self.ui.appareilGazComboBox.setItemData(0, appareil)
                self.ui.nombreAppareilGazSpinBox.setValue(int(consommation[2]))
                self.ui.nombreHeureDUtilisationGazSpinBox.setValue(int(consommation[3]))

        self.ui.add_conso_gaz.setEnabled(False)

    def get_selected_id(self):
        """
        Récupère l'ID de l'élément sélectionné dans la table.
        :return: ID de l'élément ou None si rien n'est sélectionné.
        """
        selected_indexes = self.ui.tableView_conso_gaz.selectionModel().selectedIndexes()
        if selected_indexes:
            current_row = selected_indexes[0].row()
            return self.ui.tableView_conso_gaz.model().index(current_row, 0).data()
        return None

    def clear_input(self):
        self.ui.appareilGazComboBox.clearEditText()
        self.ui.nombreAppareilGazSpinBox.clear()
        self.ui.nombreHeureDUtilisationGazSpinBox.clear()
        self.ui.tableView_conso_gaz.clearSelection()
        self.ui.add_conso_gaz.setEnabled(True)

    def get_inputs(self):
        try:
            appareil_id = self.ui.appareilGazComboBox.currentData()[0]
            nbr_appareil = float(self.ui.nombreAppareilGazSpinBox.text()) or 0
            nbr_heures_utilisation = float(self.ui.nombreHeureDUtilisationGazSpinBox.text()) or 0
            if appareil_id and nbr_appareil > 0 and nbr_heures_utilisation >= 0:
                return ConsommationGaz(appareil_id, nbr_appareil, nbr_heures_utilisation)
            else:
                raise ValueError("Invalid input values.")
        except ValueError:
            QtWidgets.QMessageBox.warning(self.main_window, "Attention",
                                          "Veuillez saisir les informations valides de l'appareil à ajouter.")
            return None

    def delete_item(self):
        id_ = self.get_selected_id()

        if id_ is None:
            QtWidgets.QMessageBox.warning(self.main_window, "Attention",
                                          "Veuillez sélectionner un appareil à supprimer.")
            return

        # Demander une confirmation avant de supprimer
        response = QtWidgets.QMessageBox.question(self.main_window, "Confirmation",
                                                  "Êtes-vous sûr de vouloir supprimer cet appareil ?",
                                                  QtWidgets.QMessageBox.StandardButton.Yes |
                                                  QtWidgets.QMessageBox.StandardButton.No,
                                                  QtWidgets.QMessageBox.StandardButton.No)

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            row = self.get_row_from_id(id_)
            if row is not None:
                self.table_model.remove_consommation(row, id_)
                self.clear_input()
                self.ui.add_conso_gaz.setEnabled(True)
                self.calculate_consommation()

    def get_row_from_id(self, id_):
        """
        Trouve la ligne correspondant à l'ID donné.
        :param id_: ID de l'élément.
        :return: Index de la ligne ou None si l'ID n'est pas trouvé.
        """
        for row, appareil in enumerate(self.table_model.consommations):
            if appareil[0] == id_:
                return row
        return None

    @staticmethod
    def validate_app_input(consommation):
        return all([consommation.nombre_app > 0])

    def calculate_loading_items(self):
        self.table_model.load_data_items()
        self.calculate_consommation()
