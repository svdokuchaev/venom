# Реализация бота, который проводит исследовательское тестирование приложения
# TODO:
#   > реализовать класс фильтров
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
#   > реализовать закрытие лишних окон
#   > реализовать фильтр для элементов - убирать элементы, которые не видны (координаты большие)
#   > реализовать проверку интерактивности элемента по наведению на него
#   > реализовать вспомогательный метод для дампа текущего состояния (localstorage, скриншот, etc.)
#   > реализовать фильтр недоступных методов в затемнении (e.g. z-index)
#   > для ситуаций, когда что-то идёт не так (e.g. элемент не кликается) реализовать механизм сохранения состояния для
#     последующего анализа ситуации

from element import Element
from terminal import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random, string


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


class Bot:
    def __init__(self, url, auth=True):
        """Тут передаются настройки и выполняется инициализация бота"""
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox) # linux only
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome('chromedriver/chromedriver', options=chrome_options)
        self.driver.get(url)
        if auth:
            self.auth()

    def wait(self, n=1):
        """Ждём когда закончится вся 'движуха' после наших действий и страница перейдёт в
        новое состояние"""
        command = """var performance = window.performance || 
                                       window.mozPerformance || 
                                       window.msPerformance || 
                                       window.webkitPerformance || 
                                       {}; 
                    var network = performance.getEntries() || 
                    {}; 
                    return network;"""
        prev_reqs = 0
        while True:
            # TODO: По какой-то причине умирает chromedriver в этом месте при работе с google.com и yandex.ru
            current_reqs = len(self.driver.execute_script(command))
            if current_reqs - prev_reqs < 5:
                break
            else:
                prev_reqs = current_reqs
            time.sleep(2)
        time.sleep(n)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
    def auth(self):
        self.wait(1)
        self.driver.find_element_by_css_selector("[name='auth-loginForm_login'] input").send_keys("Демо_тензор")
        self.driver.find_element_by_css_selector("[name='auth-loginForm_password'] input").send_keys("Демо123")
        self.driver.find_element_by_css_selector("button.auth-Form__submit").click()
        self.wait(2)   

    def get_elements(self):
        """Механизм генерации списка элементов, с которыми можно взаимодействовать на странице"""
        
        driver = self.driver
        log_start('Get elements: ')
        elements = driver.find_elements_by_xpath("//*")
        elements = [Element(driver, elm) for elm in elements]
        log_add('({0}) -> '.format(len(elements)))
        elements = [element for element in elements if not element.invalid]
        log_add('({0}) -> '.format(len(elements)))
        # self.wait()
        # Фильтр #1: убираем мелкие элементы, по которым сложно кликнуть
        elements = [elm for elm in elements if elm.width >= 6 and elm.height >= 6]
        # Фильтр #2: узнаём какие элементы визуально лежат внутри других
        for elm in elements:
            for other_elm in elements:
                if (elm.x <= other_elm.x) and \
                   (elm.y <= other_elm.y) and \
                   (elm.x + elm.width >= other_elm.x + other_elm.width) and \
                   (elm.y + elm.height >= other_elm.y + other_elm.height):
                    elm.childs.append(other_elm)
        log_add('({0}) -> '.format(len(elements)))
        # Фильтр #3: убираем одинаковые по размерам и положению элементы
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
        log_add('({0}) -> '.format(len(elements)))
        # Фильтр #4: убираем элементы, которые содержат в себе другие элементы
        elements = [elm for elm in elements if len(elm.childs) == 1]
        log_add('({0}) -> '.format(len(elements)))
        # Фильтр #5: Убираем невидимые эелменты    
        elements = [elm for elm in elements if elm.is_displayed()]
        log_add('({0}) -> '.format(len(elements)))
        # Фильтр #6: Убираем элементы, которые находятся ниже нижней границы окна
        window_height = driver.execute_script('return document.documentElement.clientHeight')
        elements = [elm for elm in elements if elm.y < window_height]
        log_add('({0})'.format(len(elements)))
        log_end()
        return elements
    
    def move_to(self, url):
        self.driver.execute_script('localStorage.clear()')
        self.driver.get(url)
        self.wait()
        # Если сессия была завершена - заходим заново
        # if '/auth/' in self.driver.current_url:
        #     self.auth()

    def move_by_path(self, path):
        """Итеративно прокликиваем список элементов"""
        for elm in path:
            if 'input' in elm.xpath or 'input' in elm.get_innerHTML():
                # elm.input(f'{randomword(10)}\n')
                elm.input(f'Test!!!\n')
            else:
                elm.click()
            self.wait()

    def kill(self):
        self.driver.close()

    def current_url(self):
        return self.driver.current_url

    def get_screenshot(self):
        return self.driver.get_screenshot_as_png()

    def close_all_windows(self):
        if len(self.driver.window_handles) > 1:
            for w in self.driver.window_handles[1:]:
                self.driver.switch_to.window(w)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
