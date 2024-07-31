#!/usr/bin/env python
import tkinter as tk
from enum import IntEnum as IEnum
from typing import TypedDict

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


# *********
# UI Ends, Calculation Begins
# *********

class Status(IEnum):
	NONE = 0
	SLEEP = 1
	MIRAGE = 2
	POISON = 3
	CONFUSION = 4
	CHARM = 5
	SEAL = 6
	MUD = 7
	SHROUD = 8
	ANY = -1

class Charge(IEnum):
	NONE = 0
	CHARGE = 1
	CONC = 2
	ANIMUS = 3
	GLORY = 4
	CRIT = 5
	OMNIPOTENT = 7

class Omagatoki(IEnum):
	NONE = 0
	CHARGE = 1
	DANCE = 2
	EXPLOIT = 3

class AltPowerType(IEnum):
	CRIT = 1,
	ADD = 2,
	AILMENT = 3

class DType(IEnum):
	ST = 1,
	MA = 2,
	ROOT = 3

class DemonStruct(TypedDict):
	level: int
	strength: int
	magic: int
	vitality: int
	zealot: int
	potential: int
	pleroma_n: bool
	pleroma_h: bool
	crit: bool
	weak: bool
	resist: bool
	guard: bool
	chargeType: Charge
	tarukaja: int
	rakukaja: int
	status: Status

class Calculator:
	#https://steamcommunity.com/sharedfiles/filedetails/?id=3279836265
	def __init__(self):
		self.attacker = {} # attacker demon
		self.defender = {} # defender demon
		self.envinfo = {} # battle environment/non-demon relevant info
		self.skillDict = {} # skill power constants
		self.resetStructs()

	def defineDemonStruct(self):
		ret: DemonStruct = {
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
			"chargeType": Const.NONE,
			"tarukaja": 0,
			"rakukaja": 0,
			"status": Status.NONE
		}
		return ret

	def defineSkillDict(self):
		ret = {
			#Base skills
			"Magic": 					{"basePower": 130, "type": DType.MA},
			"Ma-magic": 				{"basePower": 95, "type": DType.MA},
			"Magic-ga": 				{"basePower": 160, "type": DType.MA},
			"Ma-magic-ga": 				{"basePower": 120, "type": DType.MA},
			"Dracostrike": 				{"basePower": 200, "type": DType.ST},
			"Magic-dyne": 				{"basePower": 215, "type": DType.MA},
			"Ma-magic-dyne": 			{"basePower": 155, "type": DType.MA},
			"Magic-barion": 			{"basePower": 265, "type": DType.MA},
			"Ma-magic-barion": 			{"basePower": 185, "type": DType.MA},
			"Dance": 					{"basePower": 100, "type": DType.MA, "minhits": 2, "maxhits": 5},
			"Dance2": 					{"basePower": 150, "type": DType.MA, "minhits": 2, "maxhits": 5},
			"PierceMagic": 				{"basePower": 230, "type": DType.MA},
			"HaMudo": 					{"basePower": 140, "type": DType.MA},
			"HaMudoon": 				{"basePower": 175, "type": DType.MA},
			"Life Drain": 				{"basePower": 120, "type": DType.MA},
			"Megido": 					{"basePower": 125, "type": DType.MA},
			"Megidola": 				{"basePower": 160, "type": DType.MA},
			"Megidolaon": 				{"basePower": 190, "type": DType.MA},
			"Freikugel": 				{"basePower": 230, "type": DType.ST},
			# Magatsuhi skills
			"Twilight Wave": 			{"basePower": -700, "type": DType.ROOT},
			"Feline Fury": 				{"basePower": -440, "type": DType.ROOT},
			"Immolating Breath": 		{"basePower": -500, "type": DType.ROOT},
			"Frost Storm": 				{"basePower": -440, "type": DType.ROOT},
			"Calamitous Thunder": 		{"basePower": -420, "type": DType.ROOT},
			"Raging Whirlwind": 		{"basePower": -400, "type": DType.ROOT},
			"Holy Wrath": 				{"basePower": -480, "type": DType.ROOT},
			"Diabolical Deluge": 		{"basePower": -460, "type": DType.ROOT},
			"Big Bang": 				{"basePower": -400, "type": DType.ROOT},
			"Freikugel EX": 			{"basePower": -650, "type": DType.ROOT},
			"Soul Drain": 				{"basePower": -200, "type": DType.ROOT},
			"Tides of Chaos": 			{"basePower": -200, "minhits": 3, "maxhits": 6},
			"Torrent of Chaos": 		{"basePower": -500, "type": DType.ROOT},
			"Fountain of Chaos": 		{"basePower": -300, "type": DType.ROOT},
			"Qadistu Entropy": 			{"basePower": -250, "type": DType.ROOT},
			# Unique skills
			"Mac an Luin": 				{"basePower": 270, "type": DType.ST, "altPower": 340, "altType": AltPowerType.CRIT}
			"Gungnir": 					{"basePower": 300, "type": DType.ST},
			"Hassou Tobi":				{"basePower": 30, "type": DType.ST, "minhits": 8, "maxhits": 8, "200crit": True},
			"Andalucia":				{"basePower": 85, "type": DType.ST, "minhits": 3, "maxhits": 6},
			"Terrorblade":				{"basePower": 250, "type": DType.ST, "minhits": 1, "maxhits": 3},
			"Pestilence":				{"basePower": 170, "type": DType.ST, "altPower": 240, "altType": AltPowerType.AILMENT, "ailment": Status.ANY},
			"Hellish Slash":			{"basePower": 55, "type": DType.ST, "minhits": 4, "maxhits": 4},
			"Karnak": 					{"basePower": 150, "type": DType.ST},
			"Carnage Fang": 			{"basePower": 260, "type": DType.ST, "altPower": 400, "altType": AltPowerType.CRIT},
			"Hell Spin": 				{"basePower": 150, "type": DType.ST},
			"Dancing Strike":			{"basePower": 80, "type": DType.ST, "minhits": 3, "maxhits": 3},
			"Aramasa":					{"basePower": 20, "type": DType.ST, "minhits": 8, "maxhits": 8},
			"Wrath Tempest":			{"basePower": 30, "type": DType.ST, "altPower": 40, "altType": AltPowerType.CRIT, "minhits": 8, "maxhits": 8},
			"Headcrush": 				{"basePower": 200, "type": DType.ST},
			"Somersault": 				{"basePower": 160, "type": DType.ST},
			"Astral Saintstrike":		{"basePower": 20, "type": DType.ST, "minhits": 15, "maxhits": 15},
			"Javelin Rain": 			{"basePower": 260, "type": DType.ST},
			"Deadly Fury": 				{"basePower": 200, "type": DType.ST, "200crit": True},
			# Placeholder for making copy-paste easier
			"Placeholder": 				{"basePower": 1, "type": DType.MA}
		}
		return ret

	def setSkillPower(self, skillName : str):
		skillPower = 1
		if (self.skillDict.contains(skillName)):
			skillPower = self.skillDict[skillName]

		if (skillPower < 0):
			#Level-based damage
			self.envinfo["s_magatsuhi"] = True
	
	def resetStructs(self):
		self.attacker = self.defineDemonStruct()
		self.defender = self.defineDemonStruct()
		self.envinfo = {
			"difficulty": 3,
			"scripted": False,
			"e_mult": 1,
			"oma": Omagatoki.NONE,
			"maxhits": 1,
			"minhits": 1,
			"skillpower": 1,
			"s_magatsuhi": False,
			"strBased": False,
			"magBased": True
		}
		self.skillDict = defineSkillDict()

	def calculateDamage(self):
		return 0

	def calculateBase(self):
		return 0

	def damageText(self):
		return str(self.calculateDamage())

# ************
# App Mainloop
# ************

app = Window()
app.master.title('SMTVV Damage Calculator')
app.mainloop()