# Тут описана абстракция любого элемента на странице
# TODO:
#  > Реализовать "системный клик", когда мы воздействуем на всех родителей, кликаем просто по 
#    координатам: executor.executeScript("$(document.elementFromPoint(x, y)).click();");

class Element():
    def __init__(self, elm):
        self.invalid = False
        try:
            self.childs = []
            self.obj = elm
            self.rect = elm.rect
            self.x = self.rect['x']
            self.y = self.rect['y']
            self.width = self.rect['width']
            self.height = self.rect['height']
        except:
            self.invalid = True 