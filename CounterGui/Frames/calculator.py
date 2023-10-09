import tkinter

class CalcFrame(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.calcKeysConfig = {
			'ipadx':29,
			'ipady': 29,
			'padx': 14,
			'pady': 8
		}

		self.calcFont = {
			'font': ("Dejavu Sans",  10, 'bold'),
			'bg':'#1aff1a'
		}
		# create buttons on Order Field
		self.EntryFrame = tkinter.Frame(self)
		self.EntryFrame.pack(side=tkinter.TOP)

		self.valueEntry = tkinter.Entry(self.EntryFrame, width=54, font=('DejaVu Sans', 10))
		self.valueEntry.focus()
		self.valueEntry.grid(ipadx=10, ipady=10)

		self.buttonFrame = tkinter.Frame(self)
		self.buttonFrame.pack(side=tkinter.BOTTOM)

		self.numberFrame = tkinter.Frame(self.buttonFrame)
		self.numberFrame.grid(row=0, column=0)

		self.funcFrame = tkinter.Frame(self.buttonFrame)
		self.funcFrame.grid(row=0, column=1)

		self.btn1 = tkinter.Button(self.numberFrame, text="1", relief=tkinter.GROOVE, command=lambda: self.loadKey(1), **self.calcFont)
		self.btn1.grid(row=0, column=0, **self.calcKeysConfig)

		self.btn2 = tkinter.Button(self.numberFrame, text="2", relief=tkinter.GROOVE, command=lambda: self.loadKey(2), **self.calcFont)
		self.btn2.grid(row=0, column=1, **self.calcKeysConfig)

		self.btn3 = tkinter.Button(self.numberFrame, text="3", relief=tkinter.GROOVE, command=lambda: self.loadKey(3), **self.calcFont)
		self.btn3.grid(row=0, column=2, **self.calcKeysConfig)

		self.btn4 = tkinter.Button(self.numberFrame, text="4", relief=tkinter.GROOVE, command=lambda: self.loadKey(4), **self.calcFont)
		self.btn4.grid(row=1, column=0, **self.calcKeysConfig)

		self.btn5 = tkinter.Button(self.numberFrame, text="5", relief=tkinter.GROOVE, command=lambda: self.loadKey(5), **self.calcFont)
		self.btn5.grid(row=1, column=1, **self.calcKeysConfig)

		self.btn6 = tkinter.Button(self.numberFrame, text="6", relief=tkinter.GROOVE, command=lambda: self.loadKey(6), **self.calcFont)
		self.btn6.grid(row=1, column=2, **self.calcKeysConfig)

		self.btn7 = tkinter.Button(self.numberFrame, text="7", relief=tkinter.GROOVE, command=lambda: self.loadKey(7), **self.calcFont)
		self.btn7.grid(row=2, column=0, **self.calcKeysConfig)

		self.btn8 = tkinter.Button(self.numberFrame, text="8", relief=tkinter.GROOVE, command=lambda: self.loadKey(8), **self.calcFont)
		self.btn8.grid(row=2, column=1, **self.calcKeysConfig)

		self.btn9 = tkinter.Button(self.numberFrame, text="9", relief=tkinter.GROOVE, command=lambda: self.loadKey(9), **self.calcFont)
		self.btn9.grid(row=2, column=2, **self.calcKeysConfig)

		self.btn0 = tkinter.Button(self.numberFrame, text="0", relief=tkinter.GROOVE, command=lambda: self.loadKey(0), **self.calcFont)
		self.btn0.grid(row=3, column=0, **self.calcKeysConfig)

		self.btn00 = tkinter.Button(self.numberFrame, text="00", relief=tkinter.GROOVE, command=lambda: self.loadKey("00"), **self.calcFont)
		self.btn00.grid(row=3, column=1, **self.calcKeysConfig)

		self.btnPoint = tkinter.Button(self.numberFrame, text=".", relief=tkinter.GROOVE, command=lambda: self.loadKey("."), **self.calcFont)
		self.btnPoint.grid(row=3, column=2, **self.calcKeysConfig)

		# Functionality
		self.btnClear = tkinter.Button(self.funcFrame, text="Clear", width=5, command=self.clearEntry, relief=tkinter.GROOVE)
		self.btnClear.grid(row=0, column=0, ipady=82, pady=5, ipadx=15, padx=12)

		self.btnTotal = tkinter.Button(self.funcFrame, text="=", width=5, relief=tkinter.GROOVE, command=self.getAmount)
		self.btnTotal.grid(row=1, column=0, ipady=82, pady=5, ipadx=15, padx=12)

	def loadKey(self, key):
		# Get the Current Key
		self.currentKey: str = self.valueEntry.get()
		# delete the current Entries
		self.clearEntry()
		# Concatinate with the incoming key and render as string
		self.valueEntry.insert(0, self.currentKey + str(key))

	def clearEntry(self):
		self.valueEntry.delete(0, tkinter.END)


	def getAmount(self) -> float:
		return float(self.valueEntry.get())