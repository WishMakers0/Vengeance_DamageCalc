#!/usr/bin/env python
import tkinter as tk

class Window(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		self.createWidgets()

	def createWidgets(self):
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.mframe = MainFrame(self)
		self.mframe.anchor = tk.N
		self.mframe.grid(row=0, sticky=tk.N+tk.S+tk.W+tk.E)

		self.bframe = tk.Frame(self)
		self.bframe.anchor = tk.S
		self.bframe.grid(row=1)

		self.result = tk.Label(self.bframe, text='Bottom Text')
		self.result.anchor = tk.S
		self.result.grid()
		self.quitButton = tk.Button(self.bframe, text='Quit', command=self.quit)
		self.quitButton.anchor = tk.S
		self.quitButton.grid()

class MainFrame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)
		self.createWidgets()

	def createWidgets(self):
		self.a_frame = AttackerFrame(self)
		self.a_frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.d_frame = DefenderFrame(self)
		self.d_frame.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

class AttackerFrame(tk.LabelFrame):
	def __init__(self, master=None):
		tk.LabelFrame.__init__(self, master, labelanchor='n', text='Attacker')
		self.createWidgets()

	def createWidgets(self):
		self.topLabel = tk.Label(self, text='test')
		self.topLabel.anchor = tk.NE
		self.topLabel.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

class DefenderFrame(tk.LabelFrame):
	def __init__(self, master=None):
		tk.LabelFrame.__init__(self, master, labelanchor='n', text='Defender')
		self.createWidgets()

	def createWidgets(self):
		self.topLabel = tk.Label(self, text='test')
		self.topLabel.anchor = tk.NE
		self.topLabel.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

class Calculator:
	#https://steamcommunity.com/sharedfiles/filedetails/?id=3279836265
	def __init__(self):
		self.attacker = self.defineDemonStruct()
		self.defender = self.defineDemonStruct()
		self.envinfo = {
			"difficulty": 3,
			"scripted": False,
			"e_mult": 1
		}

	def defineDemonStruct():
		ret = {
			"level": 1,
			"strength": 1,
			"magic": 1,
			"vitality": 1,
			"zealot": False,
			"potential": 0,
			"pleroma_n": False,
			"pleroma_h": False,
			"crit": False,
			"weak": False,
			"resist": False,
			"guard": False,
			"chargeType": 0,
			"tarukaja": 0,
			"rakukaja": 0,
			"o_exploit": False,
		}
		return ret

	def calculateDamage():
		return 0

	def calculateBase():
		return 0

	def damageText():
		return str(self.calculateDamage())


app = Window()
app.master.title('SMTVV Damage Calculator')
app.mainloop()