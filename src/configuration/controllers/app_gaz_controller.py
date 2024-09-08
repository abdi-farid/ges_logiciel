from PyQt6 import QtWidgets
from src.configuration.models.app_gaz import AppareilGaz

import src._icon_rc
from src.configuration.tableModels.app_gaz_table_model import AppareilGazTableModel


class AppareilGazController:
    def __init__(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self.ui = main_window.ui

        self.table_model = AppareilGazTableModel()
        self.ui.tableView_app_gaz.setModel(self.table_model)

        # Masquer la première colonne (ID)
        self.ui.tableView_app_gaz.hideColumn(0)

        self.ui.add_app_gaz.clicked.connect(lambda: self.add_item())
        self.ui.edit_app_gaz.clicked.connect(lambda: self.update_item())
        self.ui.clear_app_gaz.clicked.connect(lambda: self.clear_input())
        self.ui.del_app_gaz.clicked.connect(lambda: self.delete_item())
        self.ui.tableView_app_gaz.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def __del__(self):
        self.clear_input()

    def add_item(self):
        appareil = self.get_inputs()
        if appareil is not None and self.validate_app_input(appareil):
            self.table_model.add_appareil(appareil)
            self.clear_input()

    def update_item(self):
        id_ = self.get_selected_id()

        if id_ is None:
            QtWidgets.QMessageBox.warning(self.main_window, "Attention",
                                          "Veuillez sélectionner un appareil à modifier.")
            return

        appareil = self.get_inputs()

        # Mise à jour dans la base de données avec l'ID récupéré
        self.table_model.update_appareil(id_, appareil)

        self.clear_input()
        self.ui.add_app_gaz.setEnabled(True)

    def on_selection_changed(self):
        id_ = self.get_selected_id()

        if id_ is not None:
            # Chercher l'appareil dans la liste en fonction de l'ID
            appareil = next((item for item in self.table_model.appareils if item[0] == id_), None)

            if appareil:
                # Mettre à jour les champs de saisie avec les données de l'appareil sélectionné
                self.ui.modLeGazLineEdit.setText(appareil[1])
                self.ui.puissanceGazLineEdit.setValue(int(appareil[2]))
                self.ui.dBitNominalGazSpinBox.setValue(int(appareil[3]))

        self.ui.add_app_gaz.setEnabled(False)

    def get_selected_id(self):
        """
        Récupère l'ID de l'élément sélectionné dans la table.
        :return: ID de l'élément ou None si rien n'est sélectionné.
        """
        selected_indexes = self.ui.tableView_app_gaz.selectionModel().selectedIndexes()
        if selected_indexes:
            current_row = selected_indexes[0].row()
            return self.ui.tableView_app_gaz.model().index(current_row, 0).data()
        return None

    def clear_input(self):
        self.ui.modLeGazLineEdit.clear()
        self.ui.puissanceGazLineEdit.clear()
        self.ui.dBitNominalGazSpinBox.clear()
        self.ui.tableView_app_gaz.clearSelection()
        self.ui.add_app_gaz.setEnabled(True)

    def get_inputs(self):
        try:
            name = self.ui.modLeGazLineEdit.text()
            puissance = float(self.ui.puissanceGazLineEdit.text()) or 0
            debit_nominal = float(self.ui.dBitNominalGazSpinBox.text()) or 0
            if name and puissance > 0 and debit_nominal >= 0:
                return AppareilGaz(name=name, puissance=puissance, debit_nominal=debit_nominal)
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
                self.table_model.remove_appareil(row, id_)
                self.clear_input()
                self.ui.add_app_gaz.setEnabled(True)

    def get_row_from_id(self, id_):
        """
        Trouve la ligne correspondant à l'ID donné.
        :param id_: ID de l'élément.
        :return: Index de la ligne ou None si l'ID n'est pas trouvé.
        """
        for row, appareil in enumerate(self.table_model.appareils):
            if appareil[0] == id_:
                return row
        return None

    @staticmethod
    def validate_app_input(appareil):
        return all([len(appareil.name) > 0 and appareil.puissance > 0])
