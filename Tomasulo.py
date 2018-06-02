import queue
	

class data_bus:
	def __init__(self, name):
		self.receivers = []
		self.name = name

	def add_receivers(self, list):
		for i in range(len(list)):
			self.receivers.append(list[i])

	def send(self, info):
		# print(self.name, "len:", len(self.receivers), "info:", info)
		for i in range(len(self.receivers)):
			# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
			# self.receivers[i].push(info)
			if (self.receivers[i].name == "mult" and info and info[0] == "MUL") \
				or (self.receivers[i].name == "div" and info and info[0] == "DIV") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "ADD") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "ADDI") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "SUB") \
				or (self.receivers[i].name == "load_store" and info and info[0] == "LW") \
				or (self.receivers[i].name == "load_store" and info and info[0] == "SW"):
				self.receivers[i].push(info)
				# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
				# print("GOKU")


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
		return self.size >= self.max_size

	def clock(self):
		if not self.empty():
			for i in range(len(self.list_data_bus)):
				# print(self.name, self.list_data_bus[i].name, "info:", self.top())
				self.list_data_bus[i].send(self.top())
			self.pop()

	def add_data_bus(self, data_bus):
		self.list_data_bus.append(data_bus)

class executer:
	def __init__(self, cycles, list_data_bus):
		self.max_cycles = cyles
		self.cycles = cycles
		self.instruction = []
		self.val = 0
		self.list_data_bus = list_data_bus

	def execute(instruction):
		self.instruction = instruction

	def clock(self):
		if len(self.instruction) > 0:
			self.cycles -= 1

		if self.cycles == 0:
			self.cycles == max_cycles

			for i in range(len(self.list_data_bus)):
				self.instruction[3] = str(val)
				self.list_data_bus[i].send(self.instruction)
			
			self.instruction = []


class reservation_station(station):
	def __init__(self, name, max_size, List_data_bus, cycles):
		super().__init__(name, max_size, List_data_bus)
		self.max_cycles = cycles
		self.cycles = cycles

	def clock(self):
		if not self.empty():
			self.cycles -= 1

		if self.cycles == 0:
			self.cycles = self.max_cycles
			if not self.empty():
				for i in range(len(self.list_data_bus)):
					# print(self.name, self.list_data_bus[i].name, "info:", self.top())
					self.list_data_bus[i].send(self.top())
				self.pop()


class instructions_unity(station):
	def __init__(self, name, max_size, Data_bus):
		super().__init__(name, max_size, Data_bus)
		self.max_size = max_size

	def push(self, obj):
		self.queue.put(obj)
		self.size += 1


# class reorder_buffer(station):
# 	def __init__(self, name, max_size, List_data_bus):
# 		self.Qi = 0

class register:
	def __init__(self, name):
		self.name = name
		self.Vi = 0
		self.Qi = ""

	def issue(self, station):
		self.Qi = station

	def store(self, val):
		self.Vi = val
		self.Qi = ""

	def load(self):
		return self.Vi

	def push(info):
		if info and info[1] == self.name:
			if info[3] = "mark":
				issue(info[0])
			else:
				store(float(info[3]))


if __name__ == "__main__":
	instructions = [
					["LW", "F1", "34(R2)"],
					["LW", "F2", "45(R3)"],
					["MUL", "F0", "F2", "F4"],
					["SUB", "F5", "F1", "F2"],
					["DIV", "F0", "F3", "F1"],
					["ADD", "F1", "F5", "F2"],
				   ]


	registers = []
	for i in range(32):
		registers.append(register("R" + str(i)))


	commom_data_bus = data_bus("common_data_bus")

	load_store = reservation_station("load_store", 8, [commom_data_bus], 4)
	mult = reservation_station("mult", 3, [commom_data_bus], 3)
	div = reservation_station("div", 3, [commom_data_bus], 5)
	add_sub = reservation_station("add_sub", 3, [commom_data_bus], 1)

	commom_data_bus.add_receivers([load_store, mult, div, add_sub])

	
	load_store_bus = data_bus("load_store_bus")
	load_store_bus.add_receivers([load_store])

	operations_bus = data_bus("operations_bus")
	operations_bus.add_receivers([mult, div, add_sub])

	instructions_unity = instructions_unity("instructions_unity", 10, [load_store_bus, operations_bus])


	clock = 0
	while len(instructions) > 0:
		print("CLOCK:", clock)
		clock += 1

		if not instructions_unity.full():
			instructions_unity.push(instructions.pop(0))

		instructions_unity.clock()
		load_store.clock()
		mult.clock()
		div.clock()
		add_sub.clock()


		print(instructions_unity.name, instructions_unity.top())
		print(load_store.name, load_store.top())
		print(mult.name, mult.top())
		print(div.name, div.top())
		print(add_sub.name, add_sub.top())

		next_clock = input()



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