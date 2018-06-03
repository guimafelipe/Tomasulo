import sys
import queue
	

class data_bus:
	def __init__(self, name):
		self.receivers = []
		self.name = name

	def add_receivers(self, list):
		for i in range(len(list)):
			self.receivers.append(list[i])

	def send(self, info):
		# print(self.name, "len:", len(self.receivers), "sending info:")
		for i in range(len(self.receivers)):
			# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
			# self.receivers[i].push(info)
			# print("trying to send info to:", self.receivers[i].name)
			if (self.receivers[i].name == "mult" and info and info[0] == "MUL") \
				or (self.receivers[i].name == "div" and info and info[0] == "DIV") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "ADD") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "ADDI") \
				or (self.receivers[i].name == "add_sub" and info and info[0] == "SUB") \
				or (self.receivers[i].name == "load_store" and info and info[0] == "LW") \
				or (self.receivers[i].name == "load_store" and info and info[0] == "SW") \
				or (self.receivers[i].name[0].isdigit()):
				self.receivers[i].push(info)
				# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
				# print("GOKU")


class executer:
	def __init__(self, list_data_bus):
		self.cycles = 0
		self.instruction = []
		self.list_data_bus = list_data_bus

	def execute(self, instruction):
		if not instruction: return

		self.instruction = instruction

		if instruction[0] == "LW" or instruction[0] == "SW": self.cycles = 4
		elif instructions[0] == "MUL": self.cycles = 3
		elif instruction[0] == "DIV": self.cycles = 5
		else: self.cycles = 1
		
		if instruction[0] == "ADD" or \
			instruction[0] == "ADDI" or \
			instruction[0] == "SUB" or \
			instruction[0] == "MUL" or \
			instruction[0] == "DIV" or \
			instruction[0] == "LW" or \
			instruction[0] == "SW":

			instruction[3] = "mark"
			for i in range(len(self.list_data_bus)):
				self.list_data_bus[i].send(instruction)

	def busy(self):
		return len(self.instruction ) == 0

	def get_result(self):
		return 0

	def mark_destiny(self):
		if len(self.instruction) < 4: return
		temp = self.instruction[3]
		self.instruction[3] = "mark"
		for i in range(len(self.list_data_bus)):
			self.list_data_bus[i].send(self.instruction)
		self.instruction[3] = temp

	def clock(self):
		if len(self.instruction) > 0:
			self.cycles -= 1

			if self.cycles == 0:
				for i in range(len(self.list_data_bus)):
					self.instruction[3] = str(self.	get_result())
					self.list_data_bus[i].send(self.instruction)
				
				self.instruction = []


class adder(executer):
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

	def get_result(self):
		return int(self.instruction[2]) + int(self.instruction[3])

	def execute(self, instruction):
		if not instruction: return

		if instruction[0] != "ADD" and instruction[0] != "ADDI" and instruction[0] != "SUB":
			return

		self.instruction = instruction
		self.cycles = 1

		self.mark_destiny()


class multiplier(executer):
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

	def get_result(self):
		return int(self.instruction[2]) * int(self.instruction[3])

	def execute(self, instruction):
		if not instruction: return

		if instruction[0] != "MUL" and instruction[0] != "DIV":
			return

		self.instruction = instruction
		if instruction[0] == "MUL": self.cycles = 3
		elif instruction[0] == "DIV": self.cycles = 5

		self.mark_destiny()


class station:
	def __init__(self, name, max_size, list_data_bus):
		self.Qj = 0
		self.Qk = 0
		self.queue = queue.Queue()
		self.name = name
		self.size = 0
		self.max_size = max_size
		self.list_data_bus = list_data_bus

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


class reservation_station(station):
	def __init__(self, name, max_size, list_data_bus, executer):
		super().__init__(name, max_size, list_data_bus)
		self.executer = executer
		self.max_cycles = executer.cycles
		self.cycles = executer.cycles

	def clock(self):
		if not self.empty():
			self.executer.execute(self.top())
		self.executer.clock()
		if not self.empty():
			self.cycles -= 1

		if self.cycles == 0:
			self.cycles = self.max_cycles
			if not self.empty():
				if not self.executer.busy():
					self.executer.execute(self.top())
				self.executer.clock()
				# for i in range(len(self.list_data_bus)):
					# print(self.name, self.list_data_bus[i].name, "info:", self.top())
					# self.list_data_bus[i].send(self.top())
				self.pop()


class instructions_unity(station):
	def __init__(self, name, max_size, list_data_bus):
		super().__init__(name, max_size, list_data_bus)
		self.max_size = max_size


# class reorder_buffer(station):
# 	def __init__(self, name, max_size, List_data_bus):
# 		self.Qi = 0


class register:
	def __init__(self, name):
		self.name = name
		self.Vi = 0
		self.Qi = ""

	def issue(self, station):
		# print("asçdfknoi asdfnASDLNFODSIANFASNDFADSFINÇ - issue")
		self.Qi = station

	def store(self, val):
		# print("asçdfknoi asdfnASDLNFODSIANFASNDFADSFINÇ - store")
		self.Vi = val
		self.Qi = ""

	def load(self):
		return self.Vi

	def push(self, info):
		# print("asçdfknoi asdfnASDLNFODSIANFASNDFADSFINÇ - pushing")
		if info and (str(info[1]) == self.name):
			# print(info, self.name, info[1])
			# print("asçdfknoi asdfnASDLNFODSIANFASNDFADSFINÇ - pushing")
			if info[3] == "mark":
				self.issue(info[0])
			else:
				self.store(float(info[3]))


def bin_to_int(b):
	ans = 0
	for i in range(len(b)-1, -1, -1):
		ans += int(b[i]) * 2**(len(b) - 1 - i)
	return ans


def read(Dict, instruction):
	# 00100000000010100000000001100100
	# ; I1: addi R10,R0,100
	ans = []
	if Dict[instruction[:6]] == "R":
		ans.append(Dict["R" + instruction[26:32]])
		ans.append(bin_to_int(instruction[16:21]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[11:16]))

	else:
		ans.append(Dict[instruction[:6]])
		ans.append(bin_to_int(instruction[11:16]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[16:32]))

	return ans


def print_registers(list):
	for register in list:
		print(register.name, " - Vi:", register.Vi, " - Qi:", register.Qi)

if __name__ == "__main__":
	Dict = {
		"000000": "R",
		"R100000": "ADD",
		"R011000": "MUL",
		"R000000": "NOP",
		"R100010": "SUB",
		"001000": "ADDI",
		"000101": "BEQ",
		"000111": "BLE",
		"000100": "BNE",
		"000010": "JMP",
		"100011": "LW",
		"101011": "SW"
	}

	# instructions = [
	# 				["LW", "F1", "34(R2)"],
	# 				["LW", "F2", "45(R3)"],
	# 				["MUL", "F0", "F2", "F4"],
	# 				["SUB", "F5", "F1", "F2"],
	# 				["DIV", "F0", "F3", "F1"],
	# 				["ADD", "F1", "F5", "F2"],
	# 			   ]
	
	instructions = []

	with open('input.txt') as file_in:
		for line in file_in:
			if line[0] == '\n':
				print()
				break
			if line[0] == ';': continue
			instructions.append(read(Dict, line))
			print(instructions[-1])


	registers = []
	for i in range(32):
		registers.append(register(str(i)))


	commom_data_bus = data_bus("common_data_bus")
	commom_data_bus.add_receivers(registers)


	load_store = reservation_station("load_store", 8, [commom_data_bus], executer([commom_data_bus]))

	multiplier = multiplier([commom_data_bus])
	mult = reservation_station("mult", 3, [commom_data_bus], multiplier)
	div = reservation_station("div", 3, [commom_data_bus], multiplier)

	adder = adder([commom_data_bus])
	add_sub = reservation_station("add_sub", 3, [commom_data_bus], adder)

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
		print_registers(registers)

		press_enter = input()


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


	# Fazer o execute de cada instrução