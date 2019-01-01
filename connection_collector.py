import server_conn


class Runner:
	def __init__(self):
		self.connections = []

	def multi_execute(self, command):
		results = {}
		for connection in self.connections:
			stdin = connection.execute(command)
			results[str(connection.get_address())] = stdin
			for i in range(0, len(stdin)):
				print(stdin[i])
		return results

	def add_connection(self, connection):
		self.connections.append(connection)

	def get_connection(self, address):
		for connection in self.connections:
			if connection.get_address() == address:
				return connection

	def remove_connection(self, address):
		index = 0
		for connection in self.connections:
			if connection.get_address() == address:
				self.connections.pop(index)
			index += 1
		return "Done"
