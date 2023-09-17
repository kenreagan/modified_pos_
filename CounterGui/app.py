import tkinter
import sys
from tkinter import ttk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
import requests

CONFIG_FILE_PATH = os.path.join(
        os.path.abspath(
            os.path.dirname(
                __file__
        )
    ), 'config.env'    
)

load_dotenv(CONFIG_FILE_PATH)

BUSINESS_NAME = os.environ.get("BUSINESS_NAME")
CLIENT_IP = os.environ.get("CLIENT_IP")
IMAGE_SZ = (15, 15)

class Main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Point Of Sale Software")
        if sys.platform == "win32":
            self.state("zoomed")
        elif sys.platform == "linux"  or sys.platform == "linux2":
            self.geometry("1366x760")
        
        self.fontConfig = {
            "font": ("DejaVu Sans", 9)
        }
        
        self.buttonConfig = {
            "font": ("Dejavu Sans",  9),
            "border": 0,
            'relief': tkinter.FLAT,
            "highlightthickness": 0,
            'bg': 'white'
        }
        
        self.startApp()
        # self.authenticateStaff()

    def clearWindow(self) -> None: 
        for widgets in self.winfo_children():
            widgets.destroy()

    def loginUser(self) -> None:
        payload = {
            "email": self.emailEntry.get(),
            "password": self.passwordEntry.get()
        }
        
        # Send request to server
        # response = requests.post(f"http://{CLIENT_IP}/staff/{business}/{department}", data=payload)
        
        # if response.status_code == 200:
        self.authenticateStaff()
        # authToken = response.json().get('token')
    
    def loadSettings(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def loadClients(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def loadReport(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def logoutUser(self):
        self.startApp()
    
    def authenticateStaff(self):
        self.loginFrame = tkinter.Frame(self)
        self.loginFrame.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

        self.emailLabel = tkinter.Label(self.loginFrame, text="Username")
        self.emailLabel.grid()

        self.emailEntry = tkinter.Entry(self.loginFrame)
        self.emailEntry.grid()

        self.passwordLabel = tkinter.Label(self.loginFrame, text="Password")
        self.passwordLabel.grid()

        self.passwordEntry = tkinter.Entry(self.loginFrame)
        self.passwordEntry.grid()

        self.signInButton = tkinter.Button(self.loginFrame,
            text="Login to Counter",
            command=self.loginUser
        )
        self.signInButton.grid()

    def startApp(self):
        self.topFrame = tkinter.Frame(self)
        self.topFrame.grid(row=0, column=0)

        self.bottomFrame = tkinter.Frame(self)
        self.bottomFrame.grid(row=1, column=0)
        
        # Frames for the sections
        self.side_nav = tkinter.Frame(self.bottomFrame, bg="white", relief=tkinter.RAISED)
        self.side_nav.grid(row=0, column=0)
        
        self.sidenavConfig = {
            'ipady': 10,
            'ipadx': 20
        }

        self.homePhoto = Image.open("icons/home.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.homeIcon = ImageTk.PhotoImage(self.homePhoto)

        self.homeButton = tkinter.Button(self.side_nav, width=7, text="Home", image=self.homeIcon, compound=tkinter.TOP, command=self.load_home, **self.buttonConfig)
        self.homeButton.grid(row=0, column=0, **self.sidenavConfig)
    
        self.clientsPhoto = Image.open("icons/clients.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.clientsIcon = ImageTk.PhotoImage(self.clientsPhoto)

        self.customerButton = tkinter.Button(self.side_nav, width=7, image=self.clientsIcon,compound=tkinter.TOP, text="Clients", **self.buttonConfig)
        self.customerButton.grid(row=1, column=0, **self.sidenavConfig)

        self.cashierPhoto = Image.open("icons/cashier.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.cashierIcon = ImageTk.PhotoImage(self.cashierPhoto)

        self.cashierButton = tkinter.Button(self.side_nav, width=7, image=self.cashierIcon, compound=tkinter.TOP, text="Cashier", **self.buttonConfig)
        self.cashierButton.grid(row=2, column=0,**self.sidenavConfig)
        
        self.ordersPhoto = Image.open("icons/orders.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.ordersIcon = ImageTk.PhotoImage(self.ordersPhoto)

        self.tablesButton = tkinter.Button(self.side_nav, width=7, image=self.ordersIcon, compound=tkinter.TOP, text="Orders", **self.buttonConfig)
        self.tablesButton.grid(row=3, column=0, **self.sidenavConfig)
        
        self.reportPhoto = Image.open("icons/report.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.reportIcon = ImageTk.PhotoImage(self.reportPhoto)

        self.reportButton = tkinter.Button(self.side_nav, width=7, image=self.reportIcon, compound=tkinter.TOP, text="Report", **self.buttonConfig)
        self.reportButton.grid(row=4, column=0,**self.sidenavConfig)
        
        self.settingsPhoto = Image.open("icons/settings.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.settingsIcon = ImageTk.PhotoImage(self.settingsPhoto)

        self.settingsButton = tkinter.Button(self.side_nav, width=7, text="Settings", image=self.settingsIcon, compound=tkinter.TOP, **self.buttonConfig, command=self.loadSettings)
        self.settingsButton.grid(row=5, column=0, **self.sidenavConfig)

        self.nonButton = tkinter.Button(self.side_nav, text="", width=5, **self.buttonConfig)
        self.nonButton.grid(row=6, column=0, ipady=103, ipadx=15)
        
        self.logoutPhoto = Image.open("icons/logout.jpg").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.logoutIcon = ImageTk.PhotoImage(self.logoutPhoto)

        self.quitButton = tkinter.Button(self.side_nav, text="Logout",
            width=5, image=self.logoutIcon, compound=tkinter.TOP,
            command=self.logoutUser, **self.buttonConfig
        )
        self.quitButton.grid(row=7, column=0, **self.sidenavConfig)

        self.midnav = tkinter.Frame(self.bottomFrame)
        self.midnav.grid(row=0, column=1)

        ## Add Business Logo To the Mid Section

        self.coverimage = Image.open("images/nyama_choma.jpg").resize((750, 650), resample=Image.LANCZOS)
        self.coverLogo = ImageTk.PhotoImage(self.coverimage)

        self.labelIcon = tkinter.Label(self.midnav, image=self.coverLogo)
        self.labelIcon.grid()

        self.ordersFrame = tkinter.Frame(self.bottomFrame, relief=tkinter.RAISED)
        self.ordersFrame.grid(row=0, column=2, padx=20)

        self.customermanager = tkinter.Frame(self.ordersFrame)
        self.customermanager.grid(row=0, column=0) 
        
        self.plusPhoto = Image.open("icons/plus.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.plusicon = ImageTk.PhotoImage(self.plusPhoto)

        self.createCustomer = tkinter.Button(self.customermanager, image=self.plusicon, compound=tkinter.LEFT, text="Add Customer", **self.fontConfig, bg='#f5f4f2')
        self.createCustomer.grid(row=0, column=0, ipady=5, ipadx=20, pady=5)

        self.createOrders = tkinter.Button(self.customermanager, text="Order Queue",width=17, bg='#f5f4f2', **self.fontConfig, command=self.manageOrderQueue)
        self.createOrders.grid(row=0, column=2, ipady=5, pady=5)

        self.reloadBtn = tkinter.Button(self.customermanager, text="refresh", width=17,bg='#f5f4f2', **self.fontConfig)
        self.reloadBtn.grid(row=0, column=3, ipady=5, pady=5)

        ##### Orders Tree view
        self.style = ttk.Style()
        self.style.configure("Treeview", highlightthickness=4, bd=0, font=("DejaVu Sans", 9))
        self.style.configure("Treeview.Heading", font=('DejaVu Sans', 9, "bold"))

        self.style.layout("Treeview",
                [
                    (
                        "Treeview.treearea",
                        {'sticky':'nswe'}
                        )
                    ]
                )

        self.ordersTreeviewFrame = tkinter.Frame(self.ordersFrame)
        self.ordersTreeviewFrame.grid(row=1, column=0)

        self.orderTreeview = ttk.Treeview(self.ordersTreeviewFrame,
            style="Treeview",
            show="headings",
            height=25,
            columns=("Name", "Quantity", "Amount"),
        )
        self.orderTreeview.heading("Name", text="Name")
        self.orderTreeview.column("Name", width=160)
        self.orderTreeview.heading("Quantity", text="Quantity")
        self.orderTreeview.column("Quantity", width=160)
        self.orderTreeview.heading("Amount", text="Amount")
        self.orderTreeview.column("Amount",width=155)
        self.orderTreeview.grid(row=0, column=0)

        # Order Details
        self.totalsFrame = tkinter.Frame(self.ordersFrame)
        self.totalsFrame.grid(row=2, column=0)
        
        self.subtotalsLabel = tkinter.Label(self.totalsFrame,text="Subtotal", font=("Arial", "12", "bold"))
        self.subtotalsLabel.grid(row=0, column=0, padx=10)

        self.subtotalsAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "12", "bold"))
        self.subtotalsAmount.grid(row=0, column=1)
        
        self.taxLabel = tkinter.Label(self.totalsFrame,text="Tax",font=("Arial", "12", "bold"))
        self.taxLabel.grid(row=0, column=2)

        self.taxAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "12", "bold"))
        self.taxAmount.grid(row=0, column=3, padx=20)

        self.payableLabel = tkinter.Label(self.totalsFrame,text="Total",font=("Arial", "12", "bold"))
        self.payableLabel.grid(row=1, column=0)

        self.payableAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "12", "bold"))
        self.payableAmount.grid(row=1, column=1, padx=20)

        self.paymentFrame = tkinter.Frame(self.ordersFrame)
        self.paymentFrame.grid(row=3, column=0)

        self.holdButton = tkinter.Button(self.paymentFrame, text="Hold order", bg="#ff8000", width=30, border=0)
        self.holdButton.grid(row=0, column=0, ipady=10)

        self.proceed = tkinter.Button(self.paymentFrame, text="Proceed", bg="green", width=30, border=0)
        self.proceed.grid(row=0, column=1, ipady=10)

    def load_home(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

        self.categories = tkinter.Frame(self.midnav, bg="white")
        self.categories.grid(row=0, column=0)

        ## Product Categories
        configs = {
            'ipady': 7,
            'ipadx': 3
        }

        self.starters = tkinter.Button(self.categories, text="starter",**self.buttonConfig)
        self.starters.grid(row=0, column=0, **configs)
       
        self.starters = tkinter.Button(self.categories, text="Breakfast", **self.buttonConfig)
        self.starters.grid(row=0, column=1, **configs)
        
        self.starters = tkinter.Button(self.categories, text="Lunch",**self.buttonConfig)
        self.starters.grid(row=0, column=2, **configs)

        self.starters = tkinter.Button(self.categories, text="Supper",**self.buttonConfig)
        self.starters.grid(row=0, column=3, **configs)

        self.starters = tkinter.Button(self.categories, text="Deserts",**self.buttonConfig)
        self.starters.grid(row=0, column=4, **configs)

        self.starters = tkinter.Button(self.categories, text="Drinks", **self.buttonConfig)
        self.starters.grid(row=0, column=5, **configs)
        
        self.starters = tkinter.Button(self.categories, text="Beverages",**self.buttonConfig)
        self.starters.grid(row=0, column=6, **configs)

        self.starters = tkinter.Button(self.categories, text="Beer", **self.buttonConfig)
        self.starters.grid(row=0, column=7, **configs)

        self.starters = tkinter.Button(self.categories, text="Wine",**self.buttonConfig)
        self.starters.grid(row=0, column=8, **configs)

        self.starters = tkinter.Button(self.categories, text="Spirits", **self.buttonConfig)
        self.starters.grid(row=0, column=9, **configs)
        # buttonConfigs

        self.btnConfig = {
            'ipady': 81.1,
            'ipadx': 47,
            'padx': 8,
            'pady': 10
        }
        self.products = tkinter.Frame(self.midnav)
        self.products.grid(row=1,column=0)

        self.midButtonConfig = {
            'bg':'white',
            'border': 0
        }

        self.button_1 = tkinter.Button(self.products, text="1", **self.midButtonConfig)
        self.button_1.grid(row=0, column=0, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="2", **self.midButtonConfig)
        self.button_1.grid(row=0, column=1, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="3", **self.midButtonConfig)
        self.button_1.grid(row=0, column=2, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="4", **self.midButtonConfig)
        self.button_1.grid(row=0, column=3, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="5", **self.midButtonConfig)
        self.button_1.grid(row=0, column=4, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="6", **self.midButtonConfig)
        self.button_1.grid(row=1, column=0, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="7", **self.midButtonConfig)
        self.button_1.grid(row=1, column=1, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="8", **self.midButtonConfig)
        self.button_1.grid(row=1, column=2, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="9", **self.midButtonConfig)
        self.button_1.grid(row=1, column=3, **self.btnConfig)
        
        self.button_1 = tkinter.Button(self.products, text="10", **self.midButtonConfig)
        self.button_1.grid(row=1, column=4, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="11", **self.midButtonConfig)
        self.button_1.grid(row=2, column=0, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="12", **self.midButtonConfig)
        self.button_1.grid(row=2, column=1, **self.btnConfig)
        
        self.button_1 = tkinter.Button(self.products, text="13",**self.midButtonConfig)
        self.button_1.grid(row=2, column=2, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="14", **self.midButtonConfig)
        self.button_1.grid(row=2, column=3, **self.btnConfig)

        self.button_1 = tkinter.Button(self.products, text="15", **self.midButtonConfig)
        self.button_1.grid(row=2, column=4, **self.btnConfig)
        
    def manageOrderQueue(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

        self.orderedQueueTree= ttk.Treeview(self.midnav,show="headings", columns=(
            "Date",
            "Table no.",
            "Served By",
            "price",
            "phone_number"
        ), style="Treeview",height=32)
        self.orderedQueueTree.heading("Date", text="Date")
        self.orderedQueueTree.column("Date", width=147)
        self.orderedQueueTree.heading("Table no.", text="Table no.")
        self.orderedQueueTree.column("Table no.", width=147)
        self.orderedQueueTree.heading("Served By", text="Served By")
        self.orderedQueueTree.column("Served By", width=147)
        self.orderedQueueTree.heading("price", text="price")
        self.orderedQueueTree.column("price", width=142)
        self.orderedQueueTree.heading("phone_number", text="Phone Number")
        self.orderedQueueTree.column("phone_number", width=147)
        self.orderedQueueTree.grid(padx=10)

        ## Bind right click Event to toogle payment of the pending orders

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = Main()
    app.run()
