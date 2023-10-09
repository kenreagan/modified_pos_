import tkinter

class Keyboard(tkinter.Frame):
	def __init__(self, root, widget, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.widget = widget
		self.letterBtn = [
    		['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '!', '@', '#', '$', '%', '}', '\u232B'],
    		['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '^', '&', '*', '(', ')', 'z', '{', '\u2B61'],
    		['x', 'c', 'v', 'b', 'n', 'm', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\u2573']
		]

		self.zadane = ''

		self.loadKeys()
		
	def select(self, value):
		if value == 'Space':
			self.widget.insert('end', ' ')
		elif value == "\u2573":
			self.destroy()
		elif value == "\u2B61":
			# Capitalize the next character
			pass
		elif value == "\u232B":
			# Delete the previous character
			self.curr = self.widget.get()
			self.widget.delete(0, tkinter.END)
			self.widget.insert('end', self.curr[:len(self.curr) -1])
		else:
			self.widget.insert('end', value)
			self.zadane = self.zadane + value

	def loadKeys(self):
		for i in range(len(self.letterBtn)):
			for j in range(len(self.letterBtn[i])):
				for characters in self.letterBtn[i][j]:
				    command = lambda x = characters: self.select(x)
				    if characters != 'Space':
				        tkinter.Button(self, text=characters.upper(), width=5, font=("DejaVu Sans", 10), command=command, relief=tkinter.GROOVE, bg="powder blue").grid(row=i, column=j, ipadx=4, ipady=18)
				    if characters == 'Space':
				        tkinter.Button(self, text=characters.upper(), command=command, bg="powder blue").grid(row=i, column=j)

	