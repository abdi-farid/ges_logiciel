from PyQt6.QtCore import Qt, QAbstractTableModel

from core.databse import Database

TABLE_NAME = 'appareils_electriques'
TABLE_COLUMNS = {'name': 'TEXT', 'puissance': 'REAL', 'puissance_en_veille': 'REAL', 'eppouce': 'REAL'}


class AppareilElectriqueTableModel(QAbstractTableModel):
    def __init__(self, appareils=None):
        super().__init__()
        self.appareils = []
        self.db = Database()
        self.db.create_table(TABLE_NAME, TABLE_COLUMNS)
        self.load_data_items()

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ['ID', 'Name', 'Puissance', 'Puissance en veille', 'Eppouce']
                return headers[section]
        return None

    def rowCount(self, index):
        return len(self.appareils)

    def columnCount(self, index):
        return 5  # ID,  Name, Puissance, Eppouce

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            appareil = self.appareils[index.row()]
            if index.column() == 0:
                return appareil[0]
            elif index.column() == 1:
                return appareil[1]
            elif index.column() == 2:
                return str(appareil[2])
            elif index.column() == 3:
                return str(appareil[3])
            elif index.column() == 4:
                return str(appareil[4])

    def add_appareil(self, appareil):
        self.db.add_record(TABLE_NAME, appareil.__dict__)

        self.beginResetModel()  # Notifier le modèle qu'il va être réinitialisé
        self.load_data_items()
        self.endResetModel()  # Fin de la réinitialisation du modèle

    def update_appareil(self, id_, appareil):
        self.db.update_record(TABLE_NAME, id_, appareil.__dict__)
        self.beginResetModel()  # Notifier le modèle qu'il va être réinitialisé
        self.load_data_items()
        self.endResetModel()  # Fin de la réinitialisation du modèle

    def remove_appareil(self, row, id_):
        self.db.delete_record(TABLE_NAME, id_)
        self.beginRemoveRows(self.index(0, 0), row, row)
        del self.appareils[row]
        self.endRemoveRows()

    def load_data_items(self):
        self.appareils = self.db.get_all_records(TABLE_NAME) or []
