from PyQt6 import QtWidgets
from src.configuration.models.app_electrique import AppareilElectrique
from src.configuration.tableModels.app_electrique_table_model import AppareilElectriqueTableModel

import src._icon_rc


class AppareilElectriqueController:
    def __init__(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self.ui = main_window.ui

        self.table_model = AppareilElectriqueTableModel()
        self.ui.tableWidget_app_elec.setModel(self.table_model)

        # Masquer la première colonne (ID)
        self.ui.tableWidget_app_elec.hideColumn(0)

        self.ui.add_app_elec.clicked.connect(lambda: self.add_item())
        self.ui.edit_app_elec.clicked.connect(lambda: self.update_item())
        self.ui.clear_app_elec.clicked.connect(lambda: self.clear_input())
        self.ui.del_app_elec.clicked.connect(lambda: self.delete_item())
        self.ui.tableWidget_app_elec.selectionModel().selectionChanged.connect(self.on_selection_changed)

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
        self.ui.add_app_elec.setEnabled(True)

    def on_selection_changed(self):
        id_ = self.get_selected_id()

        if id_ is not None:
            # Chercher l'appareil dans la liste en fonction de l'ID
            appareil = next((item for item in self.table_model.appareils if item[0] == id_), None)

            if appareil:
                # Mettre à jour les champs de saisie avec les données de l'appareil sélectionné
                self.ui.modLeLineEdit.setText(appareil[1])
                self.ui.puissanceSpinBox.setValue(int(appareil[2]))
                self.ui.puissanceEnVeilleSpinBox.setValue(int(appareil[3]))
                self.ui.ePPouceSpinBox.setValue(int(appareil[4]))

        self.ui.add_app_elec.setEnabled(False)

    def get_selected_id(self):
        """
        Récupère l'ID de l'élément sélectionné dans la table.
        :return: ID de l'élément ou None si rien n'est sélectionné.
        """
        selected_indexes = self.ui.tableWidget_app_elec.selectionModel().selectedIndexes()
        if selected_indexes:
            current_row = selected_indexes[0].row()
            return self.ui.tableWidget_app_elec.model().index(current_row, 0).data()
        return None

    def clear_input(self):
        self.ui.modLeLineEdit.clear()
        self.ui.puissanceSpinBox.clear()
        self.ui.puissanceEnVeilleSpinBox.clear()
        self.ui.ePPouceSpinBox.clear()
        self.ui.tableWidget_app_elec.clearSelection()
        self.ui.add_app_elec.setEnabled(True)

    def get_inputs(self):
        try:
            name = self.ui.modLeLineEdit.text()
            puissance = float(self.ui.puissanceSpinBox.text()) or 0
            puissance_en_veille = float(self.ui.puissanceEnVeilleSpinBox.text()) or 0
            eppouce = float(self.ui.ePPouceSpinBox.text()) or 0
            if name and puissance > 0 and eppouce >= 0:
                return AppareilElectrique(name=name, puissance=puissance, puissance_en_veille=puissance_en_veille,
                                          eppouce=eppouce)
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
                self.ui.add_app_elec.setEnabled(True)

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
