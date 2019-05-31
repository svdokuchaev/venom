# Реализация бота, который передвигается между состояниями приложения
# TODO:
#   > реализовать получение списка элементов через getEventListeners (ищем элементы, которые в 
#     теории отреагируют на наше действие)
#   > реализовать получение списка элементов через свойство is_displayed
#   > надёжное обращение к отдельному элементу через его локатор
#   > добавить обработку исключений при "протухании" элемента
#   > фильтровать однотонные элементы
#   > отключать таймеры и клиентские события на странице, что бы не было искажений состояний
#   > реализовать механизм самодиагностики (e.g. анализ скриншота всей страницы), что бы видеть,
#     когда фильтры убирают элементы, которые не следовало убирать
#   > написать юнит-тесты через тестовые страницы
#   > реализовать аутентификацию через POST запросы

from selenium import webdriver
from element import Element
import time


class Bot:
    def __init__(self, url):
        """Тут передаются настройки и выполняется инициализация бота"""
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        time.sleep(5)
        self.driver.find_element_by_css_selector("[name='auth-loginForm_login'] input").send_keys("Демо_тензор")
        self.driver.find_element_by_css_selector("[name='auth-loginForm_password'] input").send_keys("Демо123")
        self.driver.find_element_by_css_selector("button.auth-Form__submit").click()
        time.sleep(10)   
    def get_elements(self):
        """Механизм генерации списка элементов, с которыми можно взаимодействовать на странице"""
        driver = self.driver
        elements = driver.find_elements_by_xpath("//*")
        elements = [Element(elm) for elm in elements]
        print('Текущее число элементов: %s' % len(elements))
        elements = [element for element in elements if not rect.invalid]
        print('Текущее число элементов: %s' % len(elements))
        time.sleep(5)
        # Фильтр #1: узнаём какие элементы визуально лежат внутри других
        for elm in elements:
            for other_elm in elements:
                if (elm.x <= other_elm.x) and \
                   (elm.y <= other_elm.y) and \
                   (elm.x + elm.width >= other_elm.x + other_elm.width) and \
                   (elm.y + elm.height >= other_elm.y + other_elm.height):
                    elm.childs.append(other_elm)
        # Фильтр #2: убираем одинаковые по размерам и положению элементы
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
        # Фильтр #3: убираем элементы, которые содержат в себе другие элементы
        elements = [elm for elm in elements if len(elm.childs) == 1]
        # Фильтр #4: убираем мелкие элементы, по которым сложно кликнуть    
        elements = [elm for elm in elements if elm.width*elm.height >= 200 
                                               and elm.width >= 7 
                                               and elm.height >= 7]
        return elements