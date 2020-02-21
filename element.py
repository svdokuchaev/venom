# Тут описана абстракция любого элемента на странице
# TODO:
#  > Реализовать "системный клик", когда мы воздействуем на всех родителей, кликаем просто по 
#    координатам: executor.executeScript("$(document.elementFromPoint(x, y)).click();");


class Element:
    
    def __init__(self, driver, elm):
        self.invalid = False
        try:
            self.driver = driver
            self.childs = []
            self.obj = elm
            # self.rect = driver.execute_script('return arguments[0].getBoundingClientRect()', self.obj)
            self.rect = elm.rect
            self.x = self.rect['x']
            self.y = self.rect['y']
            self.width = self.rect['width']
            self.height = self.rect['height']
            self.xpath = self.get_xpath()
        except Exception as e:
            self.invalid = True
            
    def get_xpath(self):
        script_a = """elm = arguments[0];
                    function createXPathFromElement(elm) { 
                    var allNodes = document.getElementsByTagName('*'); 
                    for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
                    { 
                        //if (elm.hasAttribute('id')) { 
                        //        var uniqueIdCount = 0; 
                        //        for (var n=0;n < allNodes.length;n++) { 
                        //            if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++; 
                        //            if (uniqueIdCount > 1) break; 
                        //        }; 
                        //        if ( uniqueIdCount == 1) { 
                        //           segs.unshift('id("' + elm.getAttribute('id') + '")'); 
                        //           return segs.join('/'); 
                        //       } else { 
                        //           segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]'); 
                        //        } 
                        //} else 
                        if (elm.hasAttribute('class')) { 
                            segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]'); 
                        } else { 
                            for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                                if (sib.localName == elm.localName)  i++; }; 
                                segs.unshift(elm.localName.toLowerCase() + '[' + i + ']'); 
                        }; 
                    }; 
                    return segs.length ? '/' + segs.join('/') : null; 
                };
                return createXPathFromElement(elm);"""
        script_b = """elm = arguments[0];
                    function getPathTo(elm) {
                    // if (element.id!=='')
                    //     return 'id("'+element.id+'")';
                    if (elm===document.body)
                        return elm.tagName;
                    if(elm.parentNode !== null){
                    var ix= 0;
                    var siblings= elm.parentNode.childNodes;
                    for (var i= 0; i<siblings.length; i++) {
                        var sibling= siblings[i];
                        if (sibling===elm)
                            return getPathTo(elm.parentNode)+'/'+elm.tagName+'['+(ix+1)+']';
                        if (sibling.nodeType===1 && sibling.tagName===elm.tagName)
                            ix++;
                    }
                    }
                };
                return getPathTo(elm);"""
        xpath = self.driver.execute_script(script_b, self.obj)
        xpath = xpath.split('/svg')[0] # Если в пути присутствует svg, то браузер не найдёт ничего
        xpath = "//" + xpath
        return xpath
    
    def highlight(self):
        try:
            self.obj = self.driver.find_element_by_xpath(self.xpath)
            # self.driver.execute_script("arguments[0].style.backgroundColor = 'red'", self.obj)
        except Exception as e:
            print("Элемент протух :(\n {}".format(e))
        
    def click(self):
        try:
            self.driver.find_element_by_xpath(self.xpath).click()
        except Exception as e:
            print('{1}\n{0}'.format(e, self.xpath))

    def input(self, text):
        try:
            if 'input' in self.get_innerHTML():
                elm = self.driver.find_element_by_css_selector('input')
                elm.send_keys(text)
            else:
                self.driver.find_element_by_xpath(self.xpath).send_keys(text)
        except Exception as e:
            print('{1}\n{0}'.format(e, self.xpath))

    def is_displayed(self):
        try:
            return self.driver.find_element_by_xpath(self.xpath).is_displayed()
        except Exception as e:
            print('{1}\n{0}'.format(e, self.xpath))

    def get_text(self):
        try:
            result = self.driver.find_element_by_xpath(self.xpath).text
            if not result:
                result = self.driver.find_element_by_xpath(self.xpath).get_attribute('class')
            return result
        except Exception as e:
            return None

    def get_innerHTML(self):
        try:
            return self.driver.find_element_by_xpath(self.xpath).get_attribute('innerHTML')
        except Exception as e:
            return ''

    def __repr__(self):
        return self.xpath

    def __str__(self):
        return self.xpath

    def __eq__(self, other):
        if self.rect == other.rect and \
                self.xpath == other.xpath:
            return True
        return False
