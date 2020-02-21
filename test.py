from bot import Bot, randomword
from net import Net, State
from terminal import *


# TODO: Реализовать чистку папок от мусора после предыдущих прогонов
net = Net("https://another-todo-list.netlify.com/")
b = Bot(net.base_url, auth=False)
s = State(b.get_elements(), b.current_url(), b.get_screenshot())
net.base_url = s.url
net.add_node(s)
base_state = s
current_state = base_state
a = 0

while True:

	# Генерируем все возможные новые состояния
	log('Прокликиваем все элементы в текущем состоянии')
	for i, elm in enumerate(current_state.elements):
		a += 1
		if a > 10:
			break
		elm.highlight()
		# TODO: Если клик прошёл неудачно, то помечаем элемент как не живой и пропускаем итерацию
		log(f'({i}/{len(current_state.elements)}) Кликаем по элементу с текстом: {elm.get_text()}')
		if 'input' in elm.xpath or 'input' in elm.get_innerHTML():
			# elm.input(f'{randomword(10)}\n')
			elm.input(f'Test!!!\n')
		else:
			elm.click()
		b.wait()
		# TODO: Реализовать быстрое сравнение состояний по картинкам
		current_screenshot = b.get_screenshot()
		state = net.get_state_by_screenshot(current_screenshot)
		if state:
			log(f'Мы попали в уже имеющееся состояние: {state}')
			s = state
		else:
			# s = State([e for e in b.get_elements() if e not in current_state.elements],
			s = State(b.get_elements(),
					b.current_url(),
					current_screenshot)
			if len(s.elements) == 0:
				pass
			net.add_node(s)
		new_state = s
		net.add_edge(current_state, new_state, element=elm)
		b.close_all_windows()
		b.move_to(base_state.url)
		b.move_by_path(net.get_path(base_state, current_state))
		net.save_files()
	current_state.iterated = True

	# Выбираем новое состояние
	all_not_iterated_nodes = [n for n in net.G if not n.iterated and n.url == net.base_url]
	if len(all_not_iterated_nodes) == 0:
		log("Все состояния обработаны -> Завершаем работу.")
		break
	log(f'Список необработанных нод: {all_not_iterated_nodes}')
	target_state = all_not_iterated_nodes[0]

	# Перемещаемся в выбранное состояние
	b.move_to(net.base_url)
	b.move_by_path(net.get_path(base_state, target_state))
	log(f'Перемещаемся из {base_state} в {target_state}')
	current_state = target_state
