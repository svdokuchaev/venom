# ���������� ����, ������� ������������� ����� ����������� ����������
# TODO:
#   > ����������� ��������� ������ ��������� ����� getEventListeners (���� ��������, ������� � 
#     ������ ����������� �� ���� ��������)
#   > ����������� ��������� ������ ��������� ����� �������� is_displayed
#   > ������� ��������� � ���������� �������� ����� ��� �������
#   > �������� ��������� ���������� ��� "����������" ��������
#   > ����������� ���������� ��������
#   > ��������� ������� � ���������� ������� �� ��������, ��� �� �� ���� ��������� ���������
#   > ����������� �������� ��������������� (e.g. ������ ��������� ���� ��������), ��� �� ������,
#     ����� ������� ������� ��������, ������� �� ��������� �������
#   > �������� ����-����� ����� �������� ��������
#   > ����������� �������������� ����� POST �������

from selenium import webdriver
from element import Element
import time


class Bot:
    def __init__(self, url):
        """��� ���������� ��������� � ����������� ������������� ����"""
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        time.sleep(5)
        self.driver.find_element_by_css_selector("[name='auth-loginForm_login'] input").send_keys("����_������")
        self.driver.find_element_by_css_selector("[name='auth-loginForm_password'] input").send_keys("����123")
        self.driver.find_element_by_css_selector("button.auth-Form__submit").click()
        time.sleep(10)   
    def get_elements(self):
        """�������� ��������� ������ ���������, � �������� ����� ����������������� �� ��������"""
        driver = self.driver
        elements = driver.find_elements_by_xpath("//*")
        elements = [Element(elm) for elm in elements]
        print('������� ����� ���������: %s' % len(elements))
        elements = [element for element in elements if not rect.invalid]
        print('������� ����� ���������: %s' % len(elements))
        time.sleep(5)
        # ������ #1: ����� ����� �������� ��������� ����� ������ ������
        for elm in elements:
            for other_elm in elements:
                if (elm.x <= other_elm.x) and \
                   (elm.y <= other_elm.y) and \
                   (elm.x + elm.width >= other_elm.x + other_elm.width) and \
                   (elm.y + elm.height >= other_elm.y + other_elm.height):
                    elm.childs.append(other_elm)
        # ������ #2: ������� ���������� �� �������� � ��������� ��������
        for elm in elements:
            if len(elm.childs) < 2:
                continue
            same = True
            for child in elm.childs:
                if child.rect != elm.rect:
                   same = False
            if same:
                for child in elm.childs:
                    if child != elm:
                        elements.remove(child)
                elm.childs = ['same']
        # ������ #3: ������� ��������, ������� �������� � ���� ������ ��������
        elements = [elm for elm in elements if len(elm.childs) == 1]
        # ������ #4: ������� ������ ��������, �� ������� ������ ��������    
        elements = [elm for elm in elements if elm.width*elm.height >= 200 
                                               and elm.width >= 7 
                                               and elm.height >= 7]
        return elements