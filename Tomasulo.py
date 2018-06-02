import sys
import queue
	
class register:
	def __init__(self):
		self.Qi = 0


class data_bus:
	def __init__(self, name):
		self.receivers = []
		self.name = name

	def add_receivers(self, list):
		for i in range(len(list)):
			self.receivers.append(list[i])

	def send(self, info):
		# print("len:", len(self.receivers), "info:", info)
		for i in range(len(self.receivers)):
			# print("info:", info, "receiver:")
			self.receivers[i].push(info)


class station:
	def __init__(self, name, max_size, List_data_bus):
		self.Qj = 0
		self.Qk = 0
		self.queue = queue.Queue()
		self.name = name
		self.size = 0
		self.max_size = max_size
		self.list_data_bus = List_data_bus

	def push(self, obj):
		self.queue.put(obj)
		self.size += 1

	def pop(self):
		if not self.queue.empty():
			self.size -= 1
			return self.queue.get()

	def top(self):
		top = self.pop()
		self.push(top)
		return top

	def empty(self):
		return self.queue.empty()

	def full(self):
		return self.size == self.max_size

	def clock(self):
		if not self.empty():
			for i in range(len(self.list_data_bus)):
				print(self.name, self.list_data_bus[i].name, "info:", self.top())
				self.list_data_bus[i].send(self.pop())

	def add_data_bus(self, data_bus):
		self.list_data_bus.append(data_bus)


class reservation_station(station):
	def __init__(self, name, max_size, List_data_bus, Cycles):
		super().__init__(name, max_size, List_data_bus)
		self.max_cycles = Cycles
		self.cycles = Cycles

	def clock(self):
		self.cycles -= 1

		if self.cycles == 0:
			self.cycles = self.max_cycles
			if not self.empty():
				for i in range(len(self.list_data_bus)):
					print(self.name, self.list_data_bus[i].name, "info:", self.top())
					self.list_data_bus[i].send(self.pop())

class instructions_unity(station):
	def __init__(self, name, max_size, Data_bus):
		super().__init__(name, max_size, Data_bus)
		self.max_size = max_size

	def push(self, obj):
		self.queue.put(obj)
		self.size += 1


if __name__ == "__main__":
	instructions = [
					["LD", "F1", "34(R2)"],
					["LD", "F2", "45(R3)"],
					["MUL", "F0", "F2", "F4"],
					["SUB", "F5", "F1", "F2"],
					["DIV", "F0", "F3", "F1"],
					["ADD", "F1", "F5", "F2"],
				   ]

	instructions_unity = instructions_unity("instructions_unity", 10, [data_bus("load_store_bus")])

	commom_data_bus = data_bus("common_data_bus")

	load_store = reservation_station("load_store", 8, [commom_data_bus], 4)
	mult = reservation_station("mult", 3, [commom_data_bus], 3)
	div = reservation_station("div", 3, [commom_data_bus], 5)
	add_sub = reservation_station("add_sub", 3, [commom_data_bus], 1)

	commom_data_bus.add_receivers([load_store, mult, div, add_sub])

	while len(instructions) > 0:
		if not instructions_unity.full():
			instructions_unity.push(instructions.pop(0))

		instructions_unity.clock()
		load_store.clock()
		mult.clock()
		div.clock()
		add_sub.clock()


		# print("instructions_unity:", instructions_unity.top())
		# print("load_store:", load_store.top())
		# print("mult:", mult.top())
		# print("div:", div.top())
		# print("add_sub:", add_sub.top())



	# while not instructions_unity.empty():
	# 	print("instructions_unity:", instructions_unity.pop())
	# while not load_store.empty():
	# 	print("load_store:", load_store.pop())
	# while not mult.empty():
	# 	print("mult:", mult.pop())
	# while not div.empty():
	# 	print("div:", div.pop())
	# while not add_sub.empty():
	# 	print("add_sub:", add_sub.pop())