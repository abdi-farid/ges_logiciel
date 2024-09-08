import sqlite3


class Database:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)

    def create_table(self, table_name, columns):
        """
        Crée une table générique avec des colonnes et types spécifiés.

        :param table_name: Nom de la table à créer.
        :param columns: Dictionnaire où les clés sont les noms des colonnes et les valeurs sont les types de données.
        """
        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_def})"
        self.conn.execute(query)
        self.conn.commit()

    def add_record(self, table_name, record):
        """
        Ajoute un enregistrement dans une table générique.

        :param table_name: Nom de la table.
        :param record: Dictionnaire où les clés sont les colonnes et les valeurs sont les valeurs à insérer.
        """
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        values = tuple(record.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.conn.execute(query, values)
        self.conn.commit()

    def get_record_by_id(self, table_name, record_id):
        """
        Récupère un enregistrement spécifique par ID.

        :param table_name: Nom de la table.
        :param record_id: ID de l'enregistrement à récupérer.
        :return: Dictionnaire représentant l'enregistrement ou None si aucun enregistrement n'est trouvé.
        """
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        cursor = self.conn.execute(query, (record_id,))
        result = cursor.fetchone()
        if result:
            # Récupérer les noms des colonnes
            columns = [desc[0] for desc in cursor.description]
            # Retourner un dictionnaire clé-valeur
            return dict(zip(columns, result))
        return None

    def get_last_inserted_id(self):
        # Exemple pour SQLite, ajustez selon votre base de données
        cursor = self.conn.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]

    def get_all_records(self, table_name):
        """
        Récupère tous les enregistrements d'une table.

        :param table_name: Nom de la table.
        :return: Liste des enregistrements.
        """
        query = f"SELECT * FROM {table_name} ORDER BY id DESC "
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def update_record(self, table_name, record_id, updates):
        """
        Met à jour un enregistrement dans une table.

        :param table_name: Nom de la table.
        :param record_id: ID de l'enregistrement à mettre à jour.
        :param updates: Dictionnaire des colonnes et des nouvelles valeurs.
        """
        updates_def = ", ".join([f"{col} = ?" for col in updates.keys()])
        values = tuple(updates.values()) + (record_id,)
        query = f"UPDATE {table_name} SET {updates_def} WHERE id = ?"
        self.conn.execute(query, values)
        self.conn.commit()

    def delete_record(self, table_name, record_id):
        """
        Supprime un enregistrement d'une table.

        :param table_name: Nom de la table.
        :param record_id: ID de l'enregistrement à supprimer.
        """
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self.conn.execute(query, (record_id,))
        self.conn.commit()

    def execute_query(self, query, params=None):
        """
        Exécute une requête SQL générique avec ou sans paramètres.

        :param query: La requête SQL à exécuter.
        :param params: Un tuple de paramètres à passer à la requête (facultatif).
        :return: Les résultats de la requête sous forme de liste si applicable, sinon None.
        """
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()

        # Retourne les résultats si la requête est un SELECT
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        return None

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()
