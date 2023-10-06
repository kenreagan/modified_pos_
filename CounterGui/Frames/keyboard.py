import tkinter

class Keyboard(tkinter.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.letterBtn = [
    		'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    		'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
    		'z', 'x', 'c', 'v', 'b', 'n', 'm'
		]

		self.zadane = ''

		self.loadKeys()
		
		def select(self, value, entry):
			global zadane
			if value == 'Space':
				entry.insert('end', ' ')
			else:
				entry.insert('end', value)
				self.zadane = self.zadane + value

		def loadKeys(self):
			self.radek = 3 #row
			self.sloupec = 0 #column

			for button in self.letterBtn:
			    command = lambda x=button: select(x)
			    if button != 'Space':
			        tkinter.Button(klavesnice, text=button, width=5, font=("DejaVu Sans", 9, "bold"),
			                  bg='powder blue', command=command, padx=3.5, pady=3.5, bd=5
			                 ).grid(row=self.radek, column=self.sloupec)
			    if button == 'Space':
			        tkinter.Button(klavesnice, text=button, command=command).grid(row=5, column=sloupec)
			    selfsloupec += 1
			    # Specify the keyboard layout
			    if self.sloupec > 9 and self.radek == 3:
			        self.sloupec = 0
			        self.radek += 1
			    if self.sloupec > 8 and self.radek == 4:
			        self.sloupec = 0
			        self.radek += 1
