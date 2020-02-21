import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams
import uuid
from terminal import *
rcParams.update({'figure.autolayout': True})

#  TODO: реализовать механизм исключения элементов, по которым при взаимодействии возникло исключение


class Net:

    def __init__(self, base_url=''):
        self.G = nx.MultiDiGraph()
        self.base_url = base_url
        self.edge_count = 0

    def add_node(self, state):
        self.G.add_node(state)
        self.G.nodes[state]['Label Text'] = state.imsize
        log(f'Добавлено новое состояние: {state.url} | {state.imsize} | {len(state.elements)}')

    def nodes(self):
        return self.G.nodes()

    def add_edge(self, source, target, element):
        self.G.add_edge(source, target, element=element, key=self.edge_count)
        self.edge_count += 1

    def get_path(self, source, target):
        """
        Возвращаем список элементов, по которым нужно кликать
        """
        path = []
        p = nx.shortest_path(self.G, source=source, target=target)
        for i, n in enumerate(p):
            if i < len(p) - 1:
                edge_dict = self.G.get_edge_data(n, p[i + 1])
                path.append(edge_dict[list(edge_dict.keys())[0]]['element'])
        return path

    def save_files(self):
        plt.cla()  # Нужно очистить канвас, иначе новое состояние графа будет нарисовано поверх текущего
        labels = {}
        for node in self.G.nodes():
            labels[node] = node.url
        # plt.subplot(121)
        nx.draw(self.G, with_labels=True)
        # nx.draw_networkx_labels(G,nx.spring_layout(G),labels,font_size=6,font_color='r')
        # plt.tight_layout()
        plt.savefig("path.png")
        S = self.G.copy()
        for u, v, d in S.edges(data=True):
            d['element'] = d['element'].xpath
        nx.write_graphml(S, "test.graphml")

    def get_state_by_screenshot(self, current_screenshot):
        for node in self.nodes():
            if abs(node.imsize - len(current_screenshot)) < 5:
                return node
        return False


class State:

    def __init__(self, elements, url='', screenshot=b''):
        self.elements = elements
        self.hash = hash(''.join([x.xpath for x in elements]))
        self.url = url
        # self.screenshot_name = uuid.uuid4()
        self.imsize = len(screenshot)
        self.screenshot_name = self.imsize
        with open('screenshots/%s.png' % self.screenshot_name, 'wb') as f:
            f.write(screenshot)
        self.iterated = False

    def __repr__(self):
        return str(self.imsize)

    def __str__(self):
        return str(self.imsize)

    def get_screenshot(self):
        with open('screenshots/%s.png' % self.screenshot_name, 'rb') as f:
            screenshot = f.read()
        return screenshot

    def __eq__(self, other):
        if abs(self.imsize - other.imsize) < 1:
            return True
        return False

    def __hash__(self):
        return self.hash


class Transition:

    def __init__(self, element):
        self.element = element