from tkinter import *
from tkinter import ttk
from itertools import cycle
from paramiko import ssh_exception
from time import sleep

import server_conn
import connection_collector


class MainWindow(Frame):
	def __init__(self, window):
		self.rowcount = 0
		self.collector = connection_collector.Runner()
		super(MainWindow, self).__init__()
		self.window = window
		window.title("Multiplex SSH")

		tab_control = ttk.Notebook(window)

		self.tab1 = ttk.Frame(tab_control)

		self.tab2 = ttk.Frame(tab_control)

		tab_control.add(self.tab1, text='Options')

		tab_control.add(self.tab2, text='Console')

		self.lbl1 = Label(self.tab1, text='label1')

		self.lbl1.grid(column=0, row=0)

		self.lbl2 = Label(self.tab2, text='label2')

		self.lbl2.grid(column=0, row=0)

		tab_control.pack(expand=1, fill='both')

		self.greet_button = Button(self.lbl1, text="New connection", command=self.add_server_popup, padx=20)
		self.greet_button.pack()

		"""self.text_list = ["Line 1", "Line 2", "Line 3"]
		self.textiter = cycle(self.text_list)"""
		self.txt = StringVar()
		self.command = StringVar()
		self.root_entry = Entry(self.lbl2, textvariable=self.txt)
		self.root_entry.pack(fill="x", side=BOTTOM)
		self.root_entry.bind("<Return>", self.execute_command)
		self.root_text = Text(self.lbl2)
		self.root_text.pack()
		self.root_text.bind("<Insert>", self.insert_all)
		self.new_list = []

	def add_server_popup(self):
		self.win = Toplevel()
		self.win.wm_title("New connection")
		password = StringVar()
		name = StringVar()
		ip = StringVar()
		username = StringVar()
		port = StringVar()

		Label(self.win, text="Name:").grid(row=0, column=0)
		Entry(self.win, width=43, textvariable=name).grid(row=0, column=1)

		Label(self.win, text="Port:").grid(row=0, column=2)
		Entry(self.win, width=10, textvariable=port).grid(row=0, column=3)

		Label(self.win, text="IP:").grid(row=1, column=0)
		Entry(self.win, width=60, textvariable=ip).grid(row=1, column=1, columnspan=4)

		Label(self.win, text="Username:").grid(row=3, column=0)
		Entry(self.win, width=60, textvariable=username).grid(row=3, column=1, columnspan=3)

		Label(self.win, text="Password:").grid(row=4, column=0)
		pwdBox = Entry(self.win, width=60, textvariable=password, show="*")
		pwdBox.grid(row=4, column=1, columnspan=4)
		pwdBox.bind("<Return>", lambda event:
		self.greet(password, name, ip, username, port))

		Button(self.win, text="Okay", command=lambda: self.greet(password, name, ip, username, port), width=60).grid(
			columnspan=4, row=5, column=0)

	def greet(self, password, name, ip, username, port):
		status = 0
		self.win.destroy()
		try:
			conn = server_conn.RemoteServer(password=password.get(), address=ip.get())
			self.collector.add_connection(conn)
		except TimeoutError:
			status = 1
		except ssh_exception.NoValidConnectionsError:
			status = 2
		self.rowcount += 1
		localcount = self.rowcount
		Label(self.tab1, text=str(name.get()), padx=50).grid(row=self.rowcount, column=0)
		Label(self.tab1, text=str(ip.get() + ":" + port.get()), padx=100).grid(row=self.rowcount, column=1)
		if status == 0:
			Label(self.tab1, text="Connected", padx=20, fg="green").grid(row=self.rowcount, column=2)
		elif status == 1:
			Label(self.tab1, text="Cred error", padx=20, fg="yellow").grid(row=self.rowcount, column=2)
		else:
			Label(self.tab1, text="Error", padx=20, fg="red").grid(row=self.rowcount, column=2)
		Button(self.tab1, text="Edit", padx=20).grid(row=self.rowcount, column=3)
		Button(self.tab1, text="Remove", fg="red", padx=20, command=lambda: self.remove_entry(localcount)).grid(
			row=self.rowcount,
			column=4)

	def cycle_text(self, arg=None):
		t = next(self.textiter)
		self.txt.set(t)
		self.root_text.insert("end", t + "\n")
		self.root_text.see(END)
		self.new_list.append(self.root_text.get("end - 2 chars linestart", "end - 1 chars"))

	def execute_command(self, arg=None):
		t = self.txt.get()
		self.root_text.insert("end", "> " + t + "\n")
		self.root_text.see(END)
		self.txt.set("")
		result = self.collector.multi_execute(t)
		for i in range(0, len(result.keys())):
			resultParser = result[list(result.keys())[i]]
			self.root_text.insert("end", "------------------\n")
			self.root_text.insert("end", str(list(result.keys())[i]) + ": " + "\n")
			self.root_text.insert("end", "------------------\n")
			for d in resultParser:
				self.root_text.insert("end", d)
			self.root_text.see(END)

	def insert_all(self, arg):
		self.root_text.insert("end", "".join([s.strip() for s in self.new_list]))

	def remove_entry(self, row):
		counter = 0
		for label in self.tab1.grid_slaves():
			if int(label.grid_info()["row"]) == row:
				if counter == 3:
					incounter = 0
					for conn in self.collector.connections:
						if conn.get_address() == label.cget("text").split(":", 1)[0]:
							self.collector.connections.pop(incounter)
				counter += 1
				label.grid_forget()


root = Tk()
root.style = ttk.Style()
root.style.theme_use("classic")
gui = MainWindow(root)
root.mainloop()
