from bot import Bot
import time


# Тут мы выписываем для проверки список элементов, которые не находятся при текущем алгоритме
# фильтрации
elm404 = [
    driver.find_element_by_css_selector("rect.svg-icon-quick-rect"),
    driver.find_element_by_xpath("//*[@title='Настройка вида']"), 
    driver.find_element_by_css_selector("div.icon-EmptyMessage.informers_InformersBar_icon"), 
]


for elm in elm404:
    if elm not in [o.obj for o in rectangles]:
        print(elm.get_attribute('innerHTML'))
        
        
elm404 = [o for o in rectangles if o.obj in elm404]
#ac = [o for o in rectangles if elm[2] in o.childs]

for rect in rectangles:
    if len(rect.childs) < 2:
        continue
    same = True
    for child in rect.childs:
        if child.rect != rect.rect:
           same = False
    if same:
        for child in rect.childs:
            if child != rect:
                if child in elm404:
                    print("Ваш любимые элемент сейчас будет удалёен!")
                rectangles.remove(child)
        rect.childs = ['same']

b = Bot("https://fix-online.sbis.ru/calendar.html?region_left=calendar")
        
for rect in b.get_elements():
    #driver.execute_script("arguments[0].style.border='3px solid red'", rect.obj)
    driver.execute_script("arguments[0].style.backgroundColor = 'red'", rect.obj)