class Producto:
    def __init__(self, name, unitPrice, description, quantity, limitDate, priority, finanzStat, ejecStat, id=None):
        self.id = id
        self.name = name
        self.unitPrice = unitPrice
        self.description = description
        self.quantity = quantity
        self.limitDate = limitDate
        self.priority = priority
        self.finanzStat = finanzStat
        self.ejecStat = ejecStat

  