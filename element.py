# ��� ������� ���������� ������ �������� �� ��������
# TODO:
#  > ����������� "��������� ����", ����� �� ������������ �� ���� ���������, ������� ������ �� 
#    �����������: executor.executeScript("$(document.elementFromPoint(x, y)).click();");

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