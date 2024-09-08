from PyQt6.QtCore import QAbstractTableModel, Qt

from core.databse import Database
from src.configuration.tableModels.app_gaz_table_model import TABLE_NAME as APP_GAZ_TABLE

TABLE_NAME = '_1_consommation_gaz'
TABLE_COLUMNS = {'name': 'TEXT', 'puissance': 'REAL', 'debit_nominal': 'REAL'}

creation_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appareil_id INTEGER,
    nombre_app INTEGER,
    nombre_heure_utilisation INTEGER,
    FOREIGN KEY (appareil_id) REFERENCES appareils_gaz(id) ON DELETE CASCADE
);
"""


class ConsommationGazTableModel(QAbstractTableModel):
    def __init__(self, consommations=None):
        super().__init__()
        self.consommations = []
        self.db = Database()
        self.db.execute_query(creation_query)
        self.load_data_items()

        # liste des appareils a gaz
        self.appareils = self.db.get_all_records(APP_GAZ_TABLE)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ['ID', 'Appareil', 'Nombre appareil', 'Nombre heures utilisation']
                return headers[section]
        return None

    def rowCount(self, index):
        return len(self.consommations)

    def columnCount(self, index):
        return 4

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            consommation = self.consommations[index.row()]
            if index.column() == 0:
                #return self.db.get_record_by_id(APP_GAZ_TABLE, consommation[0])
                return consommation[0]

            elif index.column() == 1:
                appareil_object = self.db.get_record_by_id(APP_GAZ_TABLE, consommation[1])
                return f'{appareil_object["name"]} ({appareil_object["puissance"]})'
            elif index.column() == 2:
                return str(consommation[2])
            elif index.column() == 3:
                return str(consommation[3])

    def add_consommation(self, consommation):
        self.db.add_record(TABLE_NAME, consommation.__dict__)

        self.beginResetModel()  # Notifier le modèle qu'il va être réinitialisé
        self.load_data_items()
        self.endResetModel()  # Fin de la réinitialisation du modèle

    def update_consommation(self, id_, consommation):
        self.db.update_record(TABLE_NAME, id_, consommation.__dict__)
        self.beginResetModel()  # Notifier le modèle qu'il va être réinitialisé
        self.load_data_items()
        self.endResetModel()  # Fin de la réinitialisation du modèle

    def remove_consommation(self, row, id_):
        self.db.delete_record(TABLE_NAME, id_)
        self.beginRemoveRows(self.index(0, 0), row, row)
        del self.consommations[row]
        self.endRemoveRows()

    def load_data_items(self):
        self.consommations = self.db.get_all_records(TABLE_NAME) or []
