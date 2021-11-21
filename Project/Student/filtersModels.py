class TypeSearch:
    def __init__(self, name, selected, url):
        self.name = name
        self.selected = selected
        self.url = url 

class ListTypeSearch:
    def __init__(self, listSelected, listUrls):
        self.list = [TypeSearch("Curso", listSelected[0], listUrls[0]), TypeSearch("Universidad", listSelected[1], listUrls[1]), 
            TypeSearch("Tutor", listSelected[2], listUrls[2]), TypeSearch("Recursos públicos", listSelected[3], listUrls[3]), 
            TypeSearch("Sesiones públicas", listSelected[4], listUrls[4])]
   