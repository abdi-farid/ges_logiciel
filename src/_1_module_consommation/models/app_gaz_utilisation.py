


class AppGazUtilisation:
    def __init__(self, appareil_id, nombre, id=None):
        """
        Initialise une instance de la classe AppGazUtilisation.

        :param appareil_id: ID de l'appareil de la table appareils_gaz.
        :param nombre: Nombre d'utilisation de l'appareil.
        :param id: ID unique de l'enregistrement (auto-généré par la base de données).
        """
        self.id = id
        self.appareil_id = appareil_id
        self.nombre = nombre

    def __repr__(self):
        return f"AppGazUtilisation(id={self.id}, appareil_id={self.appareil_id}, nombre={self.nombre})"
