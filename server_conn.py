import paramiko
from paramiko import SSHClient


class RemoteServer:
	password = ""
	user = ""
	port = 0
	address = ""
	client = SSHClient()
	name = ""

	def __init__(self, **kwargs):
		self.name = kwargs.get("name")
		self.password = kwargs.get("password")
		self.username = kwargs.get("username", "user")
		self.port = kwargs.get("port", 22)
		self.address = kwargs.get("address")
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(self.address, password=self.password, port=self.port, username=self.username)

	def execute(self, command):
		stdin, stdout, stderr = self.client.exec_command(command)
		return stdout.readlines()

	def get_address(self):
		return str(self.address)

	def __str__(self):
		return self.address

