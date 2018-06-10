import sys
import queue



class recently_used_memory:
	def __init__(self):
		self.list = []

	def push(self, item):
		if len(self.list) == 4:
			self.list.pop(0)
		self.list.append(item)

	def print(self):
		for item in self.list:
			print("adress:", item[0], "val:", item[1])


# Global variables
memory = []
clocks = 0	
PC = 0
concluded_instructions = 0
recently_used_memory


class data_bus:
	def __init__(self, name):
		self.receivers = []
		self.name = name
		self.queue = []

	def print(self):
		print(self.queue)

	def add_receivers(self, list):
		for i in range(len(list)):
			self.receivers.append(list[i])

	def send(self, info):
		if len(info) == 4: info.append("")
		# print("INFO:", info, self.name)
		self.queue.append(info)
		# print("new QUEUE:", self.queue, self.name)

	def clock(self):
		# print("QUEUE:", self.queue, self.name)
		for i in range(len(self.queue)):
			info = self.queue[i]

			if not info: continue
			# print(self.name, "len:", len(self.receivers), "sending info:")
			for i in range(len(self.receivers)):
				# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
				# self.receivers[i].push(info)
				if info[0] != "done":
				# if True:
					if (self.receivers[i].name == "mult" and info and info[0] == "MUL") \
						or (self.receivers[i].name == "div" and info and info[0] == "DIV") \
						or (self.receivers[i].name == "add_sub" and info and info[0] == "ADD") \
						or (self.receivers[i].name == "add_sub" and info and info[0] == "ADDI") \
						or (self.receivers[i].name == "add_sub" and info and info[0] == "SUB") \
						or (self.receivers[i].name == "load_store" and info and info[0] == "LW") \
						or (self.receivers[i].name == "load_store" and info and info[0] == "SW") \
						or (self.receivers[i].name == "register_bank"):
						self.receivers[i].push(info)
				elif self.receivers[i].name == "register_bank":
					self.receivers[i].push(info)
				elif isinstance(self.receivers[i], buffer) and (self.receivers[i].Qj == info[1] or self.receivers[i].Qk == info[1]):
					print("ksjdfnsjdafnKJDNSLFNSJKDNFJSDNAÇFJKNDJAFSNJASNDFNALKSDNFSD")
					if self.receivers[i].Qj == info[1]:
						self.receivers[i].Qj.clear()
						self.receivers[i].Vj = info[3]
					if self.receivers[i].Qk == info[1]:
						self.receivers[i].Qk.clear()
						self.receivers[i].Vk = info[3]
					# print(self.name, "info:", info, "receiver:", self.receivers[i].name)
					# print("GOKU")
		self.queue.clear()


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

			instruction[-1] = "mark"
			for i in range(len(self.list_data_bus)):
				self.list_data_bus[i].send(instruction)

	def busy(self):
		return len(self.instruction) > 0

	def get_result(self):
		return 0

	def mark_destiny(self):
		if not self.instruction: return

		instruction = []
		for el in self.instruction:
			instruction.append(el)

		instruction[-1] = "mark"
		for i in range(len(self.list_data_bus)):
			# print("INSTRUCTION:", instruction, self.list_data_bus[i].name)
			self.list_data_bus[i].send(instruction)
		instruction.pop()

	def clock(self):
		if len(self.instruction) > 0:
			instruction = []
			for el in self.instruction:
				instruction.append(el)

			if self.cycles > 0:
				self.cycles -= 1

			if self.cycles == 0:
				for i in range(len(self.list_data_bus)):
					# print("BEFORE:", instruction)
					instruction[3] = str(self.	get_result())
					instruction[0] = "done"
					# print("EXECUTING", instruction)
					self.list_data_bus[i].send(instruction)
				
				self.instruction.clear()

				global concluded_instructions
				concluded_instructions += 1


class loader(executer):
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

	def get_result(self, register_bank):
		if self.instruction[0] == "LW":
			address = int(self.instruction[2]) + register_bank.registers[int(self.instruction[3])].Vi
			recently_used_memory.push([address, memory[address]])
			# print("address", address, "memory:", memory[address])
			return memory[address]
		elif self.instruction[0] == "SW":
			address = int(self.instruction[2]) + int(register_bank.registers[int(self.instruction[3])].Vi)
			memory[address] = register_bank.registers[int(self.instruction[1])].Vi
			recently_used_memory.push([address, memory[address]])
			# print("address", address, "memory:", memory[address])

	def execute(self, instruction):
		if not instruction: return

		if instruction[0] != "SW" and instruction[0] != "LW":
			return

		self.instruction = instruction
		self.cycles = 4

		self.mark_destiny()

	def clock(self, register_bank):
		if len(self.instruction) > 0:

			if self.cycles > 0:
				self.cycles -= 1

			if self.cycles == 0:
				instruction = []
				for el in self.instruction:
					instruction.append(el)

				if instruction[0] == "LW":
					for i in range(len(self.list_data_bus)):
						instruction[3] = str(self.get_result(register_bank))
						instruction[0] = "done"
						# print("EXECUTING", instruction)
						self.list_data_bus[i].send(instruction)
				elif instruction[0] == "SW":
					self.get_result(register_bank)

				self.instruction.clear()

				global concluded_instructions
				concluded_instructions += 1


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

		# print("marking my DESTINY:", self.instruction)
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


class buffer:
	def __init__(self, name, max_size, list_data_bus):
		self.list = [0] * max_size
		self.Qj = [0] * max_size
		self.Qk = [0] * max_size
		self.Vj = [0] * max_size
		self.Vk = [0] * max_size
		self.name = name
		self.start = 0
		self.end = 0
		self.size = 0
		self.max_size = max_size
		self.list_data_bus = list_data_bus

	def push(self, obj):
		if self.size < self.max_size:
			self.list[self.end] = obj
			self.end = (self.end + 1) % self.max_size
			self.size += 1

	def pop(self):
		if self.size > 0:
			ans = self.list[self.start]
			self.start = (self.start + 1) % self.max_size
			self.size -= 1
			return ans

	def top(self):
		if self.size > 0:
			return self.list[self.end - 1]

	def empty(self):
		return self.size == 0

	def full(self):
		return self.size >= self.max_size

	def add_data_bus(self, data_bus):
		self.list_data_bus.append(data_bus)

	def print(self):
		for i in range(self.max_size):
			print(self.name, self.list[i], self.Vj[i], self.Vk[i], self.Qj[i], self.Qk[i])


class reservation_station(buffer):
	def __init__(self, name, max_size, list_data_bus, executer):
		super().__init__(name, max_size, list_data_bus)
		self.executer = executer

	def clock(self):
		if not self.executer.busy():
			# print("TRYING TO EXECUTE:", self.top())
			self.executer.execute(self.pop())
		self.executer.clock()
			# for i in range(len(self.list_data_bus)):
				# print(self.name, self.list_data_bus[i].name, "info:", self.top())
				# self.list_data_bus[i].send(self.top())


class instructions_unity(buffer):
	def __init__(self, name, max_size, list_data_bus):
		super().__init__(name, max_size, list_data_bus)
		self.max_size = max_size

	def clock(self):
		if not self.empty():
			for i in range(len(self.list_data_bus)):
				# print(self.name, self.list_data_bus[i].name, "info:", self.top())
				self.list_data_bus[i].send(self.top())
			self.pop()

class load_store(buffer):
	def __init__(self, name, max_size, list_data_bus, executer):
		super().__init__(name, max_size, list_data_bus)
		self.executer = executer

	def clock(self, register_bank):
		if not self.executer.busy():
			self.executer.execute(self.pop())
		self.executer.clock(register_bank)


class register:
	def __init__(self, name):
		self.name = name
		self.Vi = 0
		self.Qi = ""


class register_bank:
	def __init__(self, name):
		self.name = name
		self.registers = []	
		for i in range(32):
			self.registers.append(register(str(i)))

	def print(self):
		for register in self.registers:
			print(register.name, " - Vi:", register.Vi, " - Qi:", register.Qi)

	def push(self, info):
		# print("IN THE REGISTER_BANK:", info)
		if info[-1] == "mark":
			if info[0] == "SW":
				return
				# memory[int(info[2]) + int(info[3])] = info[0]
			else:
				if int(info[1]) != 0:
					self.registers[int(info[1])].Qi = info[0]
		elif info[0] == "SW":
			return
			# if int(info[2]) + int(info[3]) != 0:
			# 	self.registers[int(info[2]) + int(info[3])].Vi = self.registers[int(info[1])].Vi
			# 	self.registers[int(info[2]) + int(info[3])].Qi = ""
		# elif info[0] == "LW":
		# 	if int(info[1]) != 0:
		# 		self.registers[int(info[1])].Vi = self.registers[int(info[2]) + int(info[3])].Vi
		# 		self.registers[int(info[1])].Qi = ""
		else:
			if info[1] != 0:
				self.registers[int(info[1])].Vi = float(info[3])
				self.registers[int(info[1])].Qi = ""


def bin_to_int(b):
	ans = 0
	for i in range(len(b)-1, -1, -1):
		ans += int(b[i]) * 2**(len(b) - 1 - i)
	return str(ans)


def read_binary(Dict, instruction):
	# 00100000000010100000000001100100
	# ; I1: addi R10,R0,100
	ans = []
	if Dict[instruction[:6]] == "R":
		ans.append(Dict["R" + instruction[26:32]])
		ans.append(bin_to_int(instruction[16:21]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[11:16]))
		ans.append("")

	else:
		ans.append(Dict[instruction[:6]])
		ans.append(bin_to_int(instruction[11:16]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[16:32]))
		ans.append("")

	return ans


def read_assembly(Dict, instruction):
	ans = []
	instruction = instruction[:-1]

	if instruction[0] == 'P':
		ans.append(instruction[:-1])
		return ans

	I_R = instruction.split(" ")
	ans.append(I_R[0])
	R = I_R[1].split(",")
	ans.append(R[0][1:])

	if ans[0] == "LW" or ans[0] == "SW":
		R = R[-1].split("(")
		ans.append(R[0])
		ans.append(R[1][1:-1])
	else:
		ans.append(R[1][1:])
		if R[2][0] == 'R' or R[2][0] == 'P':
			R[2] = R[2][1:]
		ans.append(R[2])

	return ans


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
	
	instructions = []

	with open('benchmark.txt') as file_in:
	# with open('input.txt') as file_in:
		for line in file_in:
			if line[0] == '\n':
				print()
				break
			if line[0] == ';': continue
			# instructions.append(read_binary(Dict, line))
			instructions.append(read_assembly(Dict, line))
			print(instructions[-1])


	register_bank = register_bank("register_bank")
	register_bank.push(["ADDI", "1", "0", "3"])


	commom_data_bus = data_bus("common_data_bus")
	commom_data_bus.add_receivers([register_bank])

	loader = loader([commom_data_bus])
	load_store = load_store("load_store", 5, [commom_data_bus], loader)

	multiplier = multiplier([commom_data_bus])
	mult = reservation_station("mult", 3, [commom_data_bus], multiplier)
	div = reservation_station("div", 3, [commom_data_bus], multiplier)

	adder = adder([commom_data_bus])
	add_sub = reservation_station("add_sub", 3, [commom_data_bus], adder)

	# commom_data_bus.add_receivers([load_store, mult, div, add_sub])	

	load_store_bus = data_bus("load_store_bus")
	load_store_bus.add_receivers([load_store])

	operations_bus = data_bus("operations_bus")
	operations_bus.add_receivers([mult, div, add_sub])

	instructions_unity = instructions_unity("instructions_unity", 6, [load_store_bus, operations_bus])

	memory = [0] * 4000
	clocks = 0
	PC = 0
	concluded_instructions = 0
	recently_used_memory = recently_used_memory()
	# while len(instructions) > 0:
	while True:
		print("RUM:")
		recently_used_memory.print()
		print()
		print("CLOCKS:", clocks)
		print("PC:", PC)
		print("# of concluded instructions:", concluded_instructions)
		if concluded_instructions != 0:
			print("CPI:", round(clocks/concluded_instructions, 3))
		clocks += 1

		if (not instructions_unity.full()) and (int(PC / 4) < len(instructions)):
			instructions_unity.push(instructions[int(PC / 4)])
		PC += 4

		instructions_unity.clock()
		load_store.clock(register_bank)
		mult.clock()
		# div.clock()
		add_sub.clock()
		# print("LIST_DATA_BUS", add_sub.list_data_bus)
		# for i in range(len(add_sub.list_data_bus)):
		# 	print("DATA_BUS")
		# 	add_sub.list_data_bus[i].print()
		commom_data_bus.print()
		commom_data_bus.clock()
		load_store_bus.clock()
		operations_bus.clock()


		# print(instructions_unity.name, instructions_unity.top())
		# print(load_store.name, load_store.top())
		# print(mult.name, mult.top())
		# print(div.name, div.top())
		# print(add_sub.name, add_sub.top())
		instructions_unity.print()
		load_store.print()
		mult.print()
		# div.print()
		add_sub.print()
		register_bank.print()

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


	# Fazer o if len(.Qi) == 0: val = .Vi