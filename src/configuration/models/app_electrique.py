class AppareilElectrique:
    def __init__(self, name: str = None, puissance: float = None, puissance_en_veille: float = None,
                 eppouce: float = None):
        self.name = name
        self.puissance = puissance
        self.puissance_en_veille = puissance_en_veille
        self.eppouce = eppouce
