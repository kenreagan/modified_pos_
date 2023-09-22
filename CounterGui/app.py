import tkinter
from tkinter import messagebox
import sys
from tkinter import ttk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
import requests
from utils import (
    OrderAbc,
    OrderQueue,
    Product
)
import random
import warnings
from tkinter import ttk
from typing import Dict, Any

warnings.filterwarnings("ignore")

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
CLIENT_BUSINESS = None

# load Business
client_business_req = requests.get(f"http://{CLIENT_IP}/business?name={BUSINESS_NAME}")

if client_business_req.status_code == 200:
    CLIENT_BUSINESS = client_business_req.json()

class Main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{BUSINESS_NAME} Point Of Sale Software")
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
            'relief': tkinter.GROOVE,
            "highlightthickness": 0,
            'bg': 'white',
            'takefocus': False
        }
        self.configure(bg='white')
        self.orderQueue = OrderQueue()
        self.authenticateStaff()

    def clearWindow(self) -> None: 
        for widgets in self.winfo_children():
            widgets.destroy()

    def fetchAuthPayload(self) -> Dict[str, Any]:
        self.authPayload = {
            'department': self.departmentEntry.get(),
            "email": self.emailEntry.get(),
            "password": self.passwordEntry.get()
        }
        self.departmentEntry.delete(0,tkinter.END)
        self.emailEntry.delete(0, tkinter.END)
        self.passwordEntry.delete(0, tkinter.END)
        return self.authPayload

    def loginUser(self) -> None: 
        # Send request to server
        self.authResponse = requests.post(f"http://{CLIENT_IP}/staff/login", data=self.fetchAuthPayload())
        self.startApp()

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
        self.loginStyling = {
            'ipadx': 10,
            'ipady': 8,
            'pady': 5
        }
        self.loginFrame = tkinter.Frame(self, bg='white')
        self.loginFrame.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

        self.departmentsLabel = tkinter.Label(self.loginFrame, text="Department", fg='black', bg='white', **self.fontConfig)
        self.departmentsLabel.grid(sticky=tkinter.W)

        self.departmentEntry = ttk.Combobox(self.loginFrame,width=39)
        self.departmentEntry.grid(**self.loginStyling)

        self.emailLabel = tkinter.Label(self.loginFrame, text="Username",**self.fontConfig, fg='black', bg='white')
        self.emailLabel.grid(sticky=tkinter.W)

        self.emailEntry = tkinter.Entry(self.loginFrame, width=40)
        self.emailEntry.grid(**self.loginStyling)

        self.passwordLabel = tkinter.Label(self.loginFrame, text="Password", fg='black', bg='white', **self.fontConfig)
        self.passwordLabel.grid(sticky=tkinter.W)

        self.passwordEntry = tkinter.Entry(self.loginFrame, width=40)
        self.passwordEntry.grid(**self.loginStyling)

        self.signInButton = tkinter.Button(self.loginFrame,
            text="Authenticate Account",
            command=self.loginUser,
            width=37,
            relief=tkinter.GROOVE,
            **self.fontConfig
        )
        self.signInButton.grid(**self.loginStyling)

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
            'ipadx': 25
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

        self.tablesButton = tkinter.Button(self.side_nav, width=7, image=self.ordersIcon, compound=tkinter.TOP, text="Orders", **self.buttonConfig, command=self.viewOrders)
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
        self.labelIcon.grid(padx=2)

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
            height=23,
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

        self.orderQuantity = tkinter.Label(self.totalsFrame, text="Quantity", font=("Arial", "10", "bold"))
        self.orderQuantity.grid(row=0, column=0)

        self.orderQuantityValues = tkinter.Label(self.totalsFrame, text="0", font=("Arial", "10", "bold"))
        self.orderQuantityValues.grid(row=0, column=1)

        ### Payment Method
        self.paymentMethodFrame = tkinter.Frame(self.totalsFrame)
        self.paymentMethodFrame.grid(row=0, column=2, pady=10)

        self.paymentVar = tkinter.IntVar(self.paymentMethodFrame)

        self.cashpayLabel = tkinter.Label(self.paymentMethodFrame, text="Cash", font=("Arial", "10", "bold"))
        self.cashpayLabel.grid(row=0, column=0)

        self.cashInput= tkinter.Checkbutton(self.paymentMethodFrame, variable=self.paymentVar, command=self.preparePayment)
        self.cashInput.grid(row=0, column=1)

        self.mpesaPayLabel = tkinter.Label(self.paymentMethodFrame, text="Mpesa", font=("Arial", "10", "bold"))
        self.mpesaPayLabel.grid(row=0, column=2)

        self.mpesaVar = tkinter.IntVar(self.paymentMethodFrame)

        self.mpesaInput= tkinter.Checkbutton(self.paymentMethodFrame, variable=self.mpesaVar, command=self.preparePayment)
        self.mpesaInput.grid(row=0, column=3)

        ## Totals
        self.subtotalsLabel = tkinter.Label(self.totalsFrame,text="Subtotal", font=("Arial", "10", "bold"))
        self.subtotalsLabel.grid(row=1, column=0, padx=10)

        self.subtotalsAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.subtotalsAmount.grid(row=1, column=1)
        
        self.taxLabel = tkinter.Label(self.totalsFrame,text="Tax",font=("Arial", "10", "bold"))
        self.taxLabel.grid(row=1, column=2)

        self.taxAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.taxAmount.grid(row=1, column=3, padx=20)

        self.amountGivenEntry = tkinter.Label(self.totalsFrame, text="Amount", font=("Arial", "10", "bold"))
        self.amountGivenEntry.grid(row=2, column=0)

        self.AmountEntry = tkinter.Entry(self.totalsFrame, state=tkinter.DISABLED)
        self.AmountEntry.grid(row=2, column=1, ipady=2, padx=3)

        self.payableLabel = tkinter.Label(self.totalsFrame,text="Total",font=("Arial", "10", "bold"))
        self.payableLabel.grid(row=2, column=2)

        self.payableAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.payableAmount.grid(row=2, column=3, padx=20)

        self.paymentFrame = tkinter.Frame(self.ordersFrame)
        self.paymentFrame.grid(row=3, column=0, pady=5)

        # Functionality Buttons
        self.printerImg = Image.open("icons/printer.png").resize((12, 12), resample=Image.LANCZOS)
        self.printerIcon= ImageTk.PhotoImage(self.printerImg)

        self.printButton = tkinter.Button(self.paymentFrame, image=self.printerIcon, compound=tkinter.LEFT, text="Print Receipt", bg="#ff5e00")
        self.printButton.grid(row=0, column=0, ipady=8, ipadx=1)

        self.payImage = Image.open("icons/receivecash.png").resize((12, 12), resample=Image.LANCZOS)
        self.payIcon = ImageTk.PhotoImage(self.payImage)

        self.proceed = tkinter.Button(self.paymentFrame, text="Get Balance", bg="#bfbfbf", image=self.payIcon, compound=tkinter.LEFT)
        self.proceed.grid(row=0, column=1, ipady=8, ipadx=1)

        self.queueImg = Image.open("icons/kitchenQueue.png").resize((12, 12),resample=Image.LANCZOS)
        self.queueIcon = ImageTk.PhotoImage(self.queueImg)

        self.holdButton = tkinter.Button(self.paymentFrame, text="Queue order", compound=tkinter.LEFT, image=self.queueIcon, bg="#2fff00")
        self.holdButton.grid(row=0, column=2, ipady=8, ipadx=1)

        self.cancelImg = Image.open("icons/cancel.png").resize((12, 12), resample=Image.LANCZOS)
        self.cancelIcon= ImageTk.PhotoImage(self.cancelImg)

        self.proceed = tkinter.Button(self.paymentFrame, image=self.cancelIcon, compound=tkinter.LEFT, text="Clear Entry", bg="#cfa3a7")
        self.proceed.grid(row=0, column=3, ipady=8, ipadx=1)

    def load_home(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

        self.categories = tkinter.Frame(self.midnav, bg="white")
        self.categories.grid(row=0, column=0, padx=15)

        ## Product Categories
        self.configs = {
            'ipady': 7,
            'ipadx': 48.4
        }

        # Fetch subcategories from API
        self.subcategories = requests.get(f"http://{CLIENT_IP}/subcategories")
        # Display null buttons
        for i in range(6):
            exec("self.item_%d = tkinter.Button(self.categories, **self.buttonConfig)"%i)
            exec(f"self.item_{i}.grid(row=0, column=i, **self.configs)")

        if self.subcategories.status_code != 200:
            messagebox.showerror("Error Fetching subcategories", "There was an error fetching the products")
        else:
            self.subcategoryFilter = self.subcategories.json().get("sucategories")

            #self.starters = tkinter.Button(self.categories, text="starter",**self.buttonConfig)
            # self.starters.grid(row=0, column=0, **configs)

            for i in range(len(self.subcategoryFilter)):
                exec("self.item_%d = tkinter.Button(self.categories, **self.buttonConfig)"%i)
                exec("self.item_%d['bg'] = random.choice(['#2d725e', '#14cc91', '#ef4f2b','#07c183', '#d3b41b', '#07a2c1'])"%i)
                exec("self.item_%d['text'] = t"%self.subcategoryFilter[i]['name'])
                exec("self.item_%d['command'] = lambda: self.filterProducts(self.subcategoryFilter[i]['name'])"%i, {"__builtins__": {"self": self, "y": self.subcategoryFilter[i]['name']}})
                exec(f"self.item_{i}.grid(row=0, column=i, **self.configs)")

        # buttonConfigs
        self.btnConfig = {
            'ipady': 81.1,
            'ipadx': 53,
            'padx': 8,
            'pady': 10
        }
        self.products = tkinter.Frame(self.midnav)
        self.products.grid(row=1,column=0)

        self.midButtonConfig = {
            'bg':'white',
            'border': 0
        }

        # Fetch the products from the business
        # Create null pointer
        for i in range(3):
            for j in range(0, 5):
                exec("self.item_%d = tkinter.Button(self.products, **self.midButtonConfig)"%i)
                exec(f"self.item_{i}.grid(row=i, column=j, **self.btnConfig)")

        self.orderCommodities = requests.get(f"{CLIENT_IP}/products?business_id={BUSINESS_ID}&department_id={DEPARTMENT_ID}")
        if self.orderCommodities.status_code != 200:
            messagebox.showerror("Error fetching records", "Error fetching data, check server configurations")
        else:
            self.client_products = self.orderCommodities.json().get("products")
            # Create Buttons
            self.iteredProducts = list(zip(*[iter(self.client_products)]*5))
            
            for i in range(len(self.iteredProducts)):
                for j in range(0, len(self.iteredProducts[i])):
                    t = self.iteredProduts[i][j]["name"]
                    y = self.iteredProducts[i][j]["id"]

                    exec("self.item_%d = tkinter.Button(self.products, **self.midButtonConfig)"%i)
                    exec("self.item_%d['bg'] = random.choice(['#2d725e', '#14cc91', '#ef4f2b','#07c183', '#d3b41b', '#07a2c1'])"%i)
                    exec("self.item_%d['text'] = t"%i)
                    exec("self.item_%d['command'] = lambda: self.addItem(y)"%i, {"__builtins__": {"self": self, "y": y}})
                    exec(f"self.item_{i}.grid(row=i, column=j, **self.btnConfig)")

    def viewOrders(self):
        for widgets in  self.midnav.winfo_children():
            widgets.destroy()
        
        # Create Order view Frame
        self.clientOrderTree= ttk.Treeview(self.midnav,show="headings", columns=(
            "Date",
            "Id",
            "Quantity",
            "Amount",
            "Status",
            "Payment"
        ), style="Treeview", height=32)
        self.clientOrderTree.heading("Date", text="Date")
        self.clientOrderTree.column("Date", width=122)
        self.clientOrderTree.heading("Quantity", text="Quantity")
        self.clientOrderTree.column("Quantity", width=121)
        self.clientOrderTree.heading("Amount", text="Amount")
        self.clientOrderTree.column("Amount", width=124)
        self.clientOrderTree.heading("Status", text="Status")
        self.clientOrderTree.column("Status", width=121)
        self.clientOrderTree.heading("Payment", text="Payment")
        self.clientOrderTree.column("Payment", width=122)
        self.clientOrderTree.heading("Id", text="Id")
        self.clientOrderTree.column("Id", width=122)
        self.clientOrderTree.grid(padx=10)

    def subcategoryFilter(self, category: str):
        pass
        
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

    def addItem(self, item_id):
        # Fetch the product with id
        req = requests.get(f"{CLIENT_IP}/{BUSINESS_NAME}/product/{item_id}")
        if req.status_code == 200:
            order_item =  req.json()
        # Add item to order Queue
        order = OrderAbc(**order_item)
        self.orderQueue.add_order(order)
        # Update the totals from the payment Frame

        for items in self.order_queue:
            self.orderTreeview.insert(0, (items['name'], items['quantity'], items['amount']))

    def preparePayment(self):
        if self.paymentVar.get() == 1:
            # Change entry field status
            self.AmountEntry['state'] = tkinter.NORMAL
        
        if self.mpesaVar.get() == 1:
            # Prepare intasend with Mpesa
            # Initiate Entry for phone number
            if self.paymentVar.get() == 0:
                self.AmountEntry['state'] = tkinter.DISABLED
            
            self.clientWindow = tkinter.Toplevel()
            self.clientWindow.title("Mpesa Stk Push")
            self.clientWindow.geometry("400x350")

            ## Labels for the input
            self.phoneNumberLabel = tkinter.Label(self.clientWindow, text="Phone Number")
            self.phoneNumberLabel.grid(row=0, column=0, pady=10)

            self.phoneNumber = tkinter.Entry(self.clientWindow, width=40)
            self.phoneNumber.grid(row=1, column=0, ipady=10, pady=10)

            self.eval("tk::PlaceWindow . Center")
            self.promptButton = tkinter.Button(self.clientWindow, text="Prompt Payment", command=self.promptMpesa, **self.buttonConfig)
            self.promptButton.grid(row=2, column=0)

    def promptMpesa(self):
        pass

    def printReceipt(self):
        self.orderQueue.printReceipt(BUSINESS_NAME)
        
    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = Main()
    app.run()
