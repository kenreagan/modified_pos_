import tkinter
from tkinter import messagebox
import sys
from tkinter import ttk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
import requests
from utils import (
    OrderQueue,
    ProductQueueAbc,
    OrderedQueueAbc
)
import random
import warnings
from tkinter import ttk
from typing import Dict, Any
from intasend import APIService
import datetime
from Frames.calculator import CalcFrame
from Frames.stylings import FoodImage
from Frames.keyboard import Keyboard
import uuid
import time

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
BUSINESS_PHONE = os.environ.get("BUSINESS_PHONE")
BUSINESS_ID = os.environ.get("BUSINESS_ID")
BUSINESS_LOCATION = os.environ.get("BUSINESS_LOCATION")
CLIENT_IP = os.environ.get("CLIENT_IP")
IMAGE_SZ = (15, 15)
CLIENT_BUSINESS = None
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
INTASEND_TOKEN = os.environ.get("INTASEND_TOKEN")
PUBLISHABLE_KEY = os.environ.get("PUBLISHABLE_KEY")
# PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

# load Business
client_business_req = requests.get(f"https://{CLIENT_IP}/business?name={BUSINESS_NAME}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN})

if client_business_req.status_code == 200:
    CLIENT_BUSINESS = client_business_req.json()


PAYMENT_SERVICE = APIService(
    token=INTASEND_TOKEN,
    publishable_key=PUBLISHABLE_KEY,
    test=True
)

class Main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{BUSINESS_NAME} Point Of Sale")
        if sys.platform == "win32":
            self.state("zoomed")
        elif sys.platform == "linux"  or sys.platform == "linux2":
            self.geometry("1366x780")
        
        self.fontConfig = {
            "font": ("DejaVu Sans", 9)
        }
        self.resizable(0,0)
        self.buttonConfig = {
            "font": ("Dejavu Sans",  9),
            "border": 0,
            'relief': tkinter.GROOVE,
            "highlightthickness": 0,
            'bg': 'white',
            'takefocus': False
        }
        # self.configure(bg='white')
        self.orderQueue = OrderQueue()
        self.authenticateStaff()

    def clearWindow(self) -> None: 
        for widgets in self.winfo_children():
            widgets.destroy() 

    def fetchAuthPayload(self) -> Dict[str, Any]:
        global STAFF

        STAFF = self.emailEntry.get()

        self.authPayload = {
            "surname" : STAFF,
            "password" : self.passwordEntry.get()
        }
        self.emailEntry.delete(0, tkinter.END)
        self.passwordEntry.delete(0, tkinter.END)
        return self.authPayload

    def loginUser(self) -> None:
        global AUTH_TOKEN 
        # Send request to server
        self.authResponse = requests.post(f"https://{CLIENT_IP}/staff/login", json=self.fetchAuthPayload())
        self.keyboard.destroy()
        if self.authResponse.status_code == 200:
            AUTH_TOKEN = self.authResponse.json()['token']
            self.startApp()
        else:
            messagebox.showerror("Authentication Error", "Invalid Credentials, contact your adminstrator")
        # self.startApp()

    def loadSettings(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

        self.topSect = tkinter.Frame(self.midnav)
        self.topSect.pack(side=tkinter.TOP)

        self.complaintsBodyLabel = tkinter.Label(self.topSect, text="Message")
        self.complaintsBodyLabel.grid(row=0, column=0, sticky=tkinter.W)

        self.complaintsBody = tkinter.Text(self.topSect, width=34, height=2)
        self.complaintsBody.grid(row=1, column=0, padx=8, ipadx=10)

        self.complaintsCategoryLabel = tkinter.Label(self.topSect, text="Category")
        self.complaintsCategoryLabel.grid(row=0, column=1, sticky=tkinter.W)

        self.complaintsCategory = ttk.Combobox(self.topSect, values=("Network Errors", "Receipt Error", "Other"))
        self.complaintsCategory.grid(row=1, column=1, padx=8, ipadx=10, ipady=5)

        self.priorityLabel = tkinter.Label(self.topSect, text="Priority")
        self.priorityLabel.grid(row=2, column=0, sticky=tkinter.W)

        self.priority = ttk.Combobox(self.topSect, values=("Low", "Medium", "High"), width=43)
        self.priority.grid(row=3, column=0, sticky=tkinter.W, padx=8, ipadx=10, ipady=5)

        self.createComplaints = tkinter.Button(self.topSect, width=15, text="Raise Issue", relief=tkinter.GROOVE)
        self.createComplaints.grid(row=3, column=1, sticky=tkinter.W, padx=8, ipadx=23, ipady=5)

        self.bottomSettingsFrame = tkinter.Frame(self.midnav)
        self.bottomSettingsFrame.pack(side=tkinter.BOTTOM)

        self.foodManager = ttk.LabelFrame(self.bottomSettingsFrame, text="Manage Stock")
        self.foodManager.grid(row=0, column=0)

        self.stockLevels = ttk.LabelFrame(self.bottomSettingsFrame, text="Stock Levels Manager")
        self.stockLevels.grid(row=1, column=0, pady=20, ipadx=4)

        self.openningStockLabel = tkinter.Label(self.stockLevels, text="Openning Stock")
        self.openningStockLabel.grid(row=0, column=0, sticky=tkinter.W)

        self.openningStock = tkinter.Entry(self.stockLevels)
        self.openningStock.grid(row=1, column=0, padx=5, ipadx=10, ipady=5)

        self.closingStockLabel = tkinter.Label(self.stockLevels, text="Closing Stock")
        self.closingStockLabel.grid(row=0, column=1, sticky=tkinter.W)

        self.closingStock = tkinter.Entry(self.stockLevels)
        self.closingStock.grid(row=1, column=1, padx=5, ipadx=10, ipady=5)

        self.expectedSalesLabel = tkinter.Label(self.stockLevels, text="Expected Sales")
        self.expectedSalesLabel.grid(row=0, column=2, sticky=tkinter.W)

        self.expectedSales = tkinter.Entry(self.stockLevels)
        self.expectedSales.grid(row=1, column=2, padx=5, ipadx=10, ipady=5)

        self.confirmEntryBtn = tkinter.Button(self.stockLevels, text="Confirm Entries", relief=tkinter.GROOVE, width=19)
        self.confirmEntryBtn.grid(row=2, column=2, ipady=5, pady=10)


    def loadClients(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def loadReport(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def logoutUser(self):
        STAFF = None
        self.authenticateStaff()
    
    def authenticateStaff(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.loginStyling = {
            'ipadx': 10,
            'ipady': 8,
            'pady': 5
        }
        self.loginFrame = tkinter.Frame(self)
        self.loginFrame.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

        self.emailLabel = tkinter.Label(self.loginFrame, text="Username",**self.fontConfig)
        self.emailLabel.grid(sticky=tkinter.W)

        self.emailEntry = tkinter.Entry(self.loginFrame, relief=tkinter.SUNKEN, width=42)
        self.emailEntry.bind("<FocusIn>", self.toogleKeyboard)
        self.emailEntry.bind("<FocusOut>", self.deleteKeyBoard)
        self.emailEntry.grid(**self.loginStyling)

        self.passwordLabel = tkinter.Label(self.loginFrame, text="Password", **self.fontConfig)
        self.passwordLabel.grid(sticky=tkinter.W)

        self.passwordEntry = tkinter.Entry(self.loginFrame, relief=tkinter.SUNKEN , show="*", width=42)
        self.passwordEntry.bind("<FocusIn>", self.toogleKeyboard)
        self.passwordEntry.bind("<FocusOut>", self.deleteKeyBoard)
        self.passwordEntry.grid(**self.loginStyling)

        self.signInButton = tkinter.Button(self.loginFrame,
            text="Authenticate Account",
            command=self.loginUser,
            width=36,
            relief=tkinter.GROOVE,
            **self.fontConfig
        )
        self.signInButton.grid(**self.loginStyling)

    def startApp(self):
        self.topFrame = tkinter.Frame(self)
        self.topFrame.grid(row=0, column=0)

        self.bottomFrame = tkinter.Frame(self)
        self.bottomFrame.grid(row=1, column=0)

        self.statusBar = ttk.LabelFrame(self, text=f"{BUSINESS_NAME}", relief=tkinter.RIDGE)
        self.statusBar.grid(row=2, column=0, ipadx=2, ipady=5)

        self.loadStatus()
        
        # Frames for the sections
        self.side_nav = tkinter.Frame(self.bottomFrame, bg="white", relief=tkinter.RAISED)
        self.side_nav.grid(row=0, column=0)
        
        self.sidenavConfig = {
            'ipady': 15,
            'ipadx': 25
        }

        self.homePhoto = Image.open("icons/home.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.homeIcon = ImageTk.PhotoImage(self.homePhoto)

        self.homeButton = tkinter.Button(self.side_nav, width=7, text="Home", image=self.homeIcon, compound=tkinter.TOP, command=self.startApp, **self.buttonConfig)
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

        self.menuButton = tkinter.Button(self.side_nav, width=7, image=self.reportIcon, compound=tkinter.TOP, text="Menu", command=self.loadMenu, **self.buttonConfig)
        self.menuButton.grid(row=4, column=0,**self.sidenavConfig)
        
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
        self.categories = tkinter.Frame(self.midnav, bg="white")
        self.categories.grid(row=0, column=0, padx=15)

        ## Product Categories
        self.configs = {
            'ipady': 7,
            'ipadx': 33
        }

        # Fetch subcategories from API
        self.subcategories = ["Drinks", "Fast Foods", "Meat", "Breakfast"]
        # Display null buttons

        for i in range(len(self.subcategories)):
            exec("self.item_%d = tkinter.Button(self.categories, bg='white', text=self.subcategories[i], relief=tkinter.GROOVE)"%i)
            exec(f"self.item_{i}.grid(row=0, column=i, **self.configs)")

        # if self.subcategories.status_code != 200:
        #     messagebox.showerror("Error Fetching subcategories", "There was an error fetching the products")
        # else:
        #     self.subcategoryFilter = self.subcategories.json().get("subcategories")

        #     for i in range(len(self.subcategoryFilter)):
        #         exec("self.item_%d = tkinter.Button(self.categories, **self.buttonConfig)"%i)
        #         exec("self.item_%d['bg'] = random.choice(['#2d725e', '#14cc91', '#ef4f2b','#07c183', '#d3b41b', '#07a2c1'])"%i)
        #         exec("self.item_%d['text'] = t"%self.subcategoryFilter[i]['name'])
        #         exec("self.item_%d['command'] = lambda: self.filterProducts(self.subcategoryFilter[i]['name'])"%i, {"__builtins__": {"self": self, "y": self.subcategoryFilter[i]['name']}})
        #         exec(f"self.item_{i}.grid(row=0, column=i, **self.configs)")

        # buttonConfigs
        self.btnConfig = {
            'ipady': 81.1,
            'ipadx': 52,
            'padx': 5,
            'pady': 10
        }
        self.products = tkinter.Frame(self.midnav)
        self.products.grid(row=1, column=0)

        self.midButtonConfig = {
            'bg':'white',
            'border': 0,
            'font': ('Dejavu Sans', 9)
        }

        # Fetch the products from the business
        # Create null pointer
        for i in range(3):
            for j in range(0, 4):
                exec("self.item_%d = tkinter.Button(self.products, **self.midButtonConfig)"%i)
                exec(f"self.item_{i}.grid(row=i, column=j, **self.btnConfig)")

        if isinstance(CLIENT_BUSINESS, dict):
            self.orderCommodities = requests.get(f"https://{CLIENT_IP}/products?business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN})

            self.updateProgressBar(f"https://{CLIENT_IP}/products?business_id={BUSINESS_ID}")

            if self.orderCommodities.status_code != 200:
                 messagebox.showerror("Error fetching records", "Error fetching data, check server configurations")
            else:
                self.client_products = self.orderCommodities.json().get("products")
                # Create Buttons
                self.foodImage = Image.open("images/Food/" +random.choice(os.listdir("./images/Food/"))).resize((90, 90), resample=Image.LANCZOS)
                self.foodImageIcon = ImageTk.PhotoImage(self.foodImage)
                self.iteredProducts = list(zip(*[iter(self.client_products)]*4))
                if len(self.iteredProducts) > 0:
                    for i in range(len(self.iteredProducts)):
                        for j in range(0, len(self.iteredProducts[i])):
                            t = self.iteredProducts[i][j]["name"]
                            y = self.iteredProducts[i][j]["id"]
                            # if self.iteredProducts[i][j]['image']:
                            #     exec("self.prodBtn_%d = tkinter.Button(self.products, image=FoodImage(self.iteredProducts[i][j]['image']).get(), compound=tkinter.BOTTOM, **self.midButtonConfig)"%i)
                            exec("self.prodBtn_%d = tkinter.Button(self.products, compound=tkinter.TOP, image=self.foodImageIcon, **self.midButtonConfig)"%i)
                            exec("self.prodBtn_%d['text']  = t"%i)
                            exec("self.prodBtn_%d['command'] = lambda: self.addItem(y)"%i, {"__builtins__": {"self": self, "y": y}})
                            exec(f"self.prodBtn_{i}.grid(row=i, column=j)")

        self.ordersFrame = tkinter.Frame(self.bottomFrame, relief=tkinter.RAISED)
        self.ordersFrame.grid(row=0, column=2, padx=20)

        self.customermanager = tkinter.Frame(self.ordersFrame)
        self.customermanager.grid(row=0, column=0) 
        
        self.plusPhoto = Image.open("icons/plus.png").resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.plusicon = ImageTk.PhotoImage(self.plusPhoto)

        self.createCustomer = tkinter.Button(self.customermanager, image=self.plusicon, relief=tkinter.GROOVE, compound=tkinter.LEFT, text=" Current Queue", **self.fontConfig, command=self.viewCustomer)
        self.createCustomer.grid(row=0, column=0, ipady=6, ipadx=18, pady=5)

        self.enqueueOrders = tkinter.Button(self.customermanager, compound=tkinter.LEFT, text="Order Queue", relief=tkinter.GROOVE, width=17, command=self.manageOrderQueue, **self.fontConfig)
        self.enqueueOrders.grid(row=0, column=2, ipady=5, padx=2, pady=5)

        self.refreshImage = Image.open('./icons/refreshicon.png').resize(IMAGE_SZ, resample=Image.LANCZOS)
        self.refreshIcon = ImageTk.PhotoImage(self.refreshImage)

        self.reloadBtn = tkinter.Button(self.customermanager, command=lambda: self.updateProgressBar(f"https://{CLIENT_IP}/orders?business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN}), image=self.refreshIcon, text="refresh", compound=tkinter.LEFT, relief=tkinter.GROOVE, width=17, **self.fontConfig)
        self.reloadBtn.grid(row=0, column=3, ipady=6, pady=5, ipadx=54)

        ##### Orders Tree view
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("DejaVu Sans", 9))
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

        self.loadEntries()

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

        self.cashInput= tkinter.Checkbutton(self.paymentMethodFrame, state=tkinter.DISABLED, variable=self.paymentVar, command=self.preparePayment)
        self.cashInput.grid(row=0, column=1)

        self.mpesaPayLabel = tkinter.Label(self.paymentMethodFrame, text="Mpesa", font=("Arial", "10", "bold"))
        self.mpesaPayLabel.grid(row=0, column=2)

        self.mpesaVar = tkinter.IntVar(self.paymentMethodFrame)

        self.mpesaInput= tkinter.Checkbutton(self.paymentMethodFrame, variable=self.mpesaVar, state=tkinter.DISABLED, command=self.preparePayment)
        self.mpesaInput.grid(row=0, column=3)

        ## Totals
        self.subtotalsLabel = tkinter.Label(self.totalsFrame,text="Subtotal", font=("Arial", "10", "bold"))
        self.subtotalsLabel.grid(row=1, column=0, padx=10)

        self.subtotalsAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.subtotalsAmount.grid(row=1, column=1)
        
        self.taxLabel = tkinter.Label(self.totalsFrame,text="Tax",font=("Arial", "10", "bold"))
        self.taxLabel.grid(row=1, column=2, padx=5)

        self.taxAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.taxAmount.grid(row=1, column=3, padx=14)

        self.amountGivenEntry = tkinter.Label(self.totalsFrame, text="Balance", font=("Arial", "10", "bold"))
        self.amountGivenEntry.grid(row=2, column=0, padx=10)

        self.AmountEntryLabel = tkinter.Label(self.totalsFrame, text="Ksh. 0.00", font=("Arial", "10", "bold"))
        self.AmountEntryLabel.grid(row=2, column=1, ipady=2, padx=3)

        self.payableLabel = tkinter.Label(self.totalsFrame,text="Total",font=("Arial", "10", "bold"))
        self.payableLabel.grid(row=2, column=2)

        self.payableAmount = tkinter.Label(self.totalsFrame, text="Ksh. 0.00",font=("Arial", "10", "bold"))
        self.payableAmount.grid(row=2, column=3, padx=5)

        self.paymentFrame = tkinter.Frame(self.ordersFrame)
        self.paymentFrame.grid(row=3, column=0, pady=5)

        # Functionality Buttons
        self.printerImg = Image.open("icons/printer.png").resize((10, 10), resample=Image.LANCZOS)
        self.printerIcon= ImageTk.PhotoImage(self.printerImg)

        self.printButton = tkinter.Button(self.paymentFrame, image=self.printerIcon, relief=tkinter.GROOVE, compound=tkinter.TOP, text="Print Receipt", state=tkinter.DISABLED, command=self.printReceipt)
        self.printButton.grid(row=0, column=0, ipady=5, ipadx=45 , padx=5)
        
        self.queueImg = Image.open("icons/kitchenQueue.png").resize((10, 10),resample=Image.LANCZOS)
        self.queueIcon = ImageTk.PhotoImage(self.queueImg)

        self.holdButton = tkinter.Button(self.paymentFrame, state=tkinter.DISABLED, text="Queue order", relief=tkinter.GROOVE, compound=tkinter.TOP, image=self.queueIcon, command=self.AddQueue)
        self.holdButton.grid(row=0, column=2, ipady=5, ipadx=20, padx=5)

        self.cancelImg = Image.open("icons/cancel.png").resize((10, 10), resample=Image.LANCZOS)
        self.cancelIcon= ImageTk.PhotoImage(self.cancelImg)

        self.clearOrderBtn = tkinter.Button(self.paymentFrame, image=self.cancelIcon, state=tkinter.DISABLED, relief=tkinter.GROOVE, compound=tkinter.TOP, text="Clear Entry", command=self.clearOrders)
        self.clearOrderBtn.grid(row=0, column=3, ipady=5, ipadx=20, padx=5)

    def ManageOrders(self, event):
        self.menuPopup = tkinter.Menu(self, tearoff=0)
        iid = self.orderTreeview.identify_row(event.y)

        if iid:
            self.orderTreeview.selection_set(iid)
            self.menuPopup.add_command(label="Delete order", command=lambda: self.deleteOrder(self.orderTreeview.item(iid)['values'][0]))
            self.menuPopup.tk_popup(event.x_root, event.y_root, 0)

    def deleteOrder(self, order):
        self.orderQueue.deleteOrder(order)

        # reload the Treeview
        self.reloadOrderTreeView()

    def resetTotals(self):
        # Reset Totals text values to zero
        self.subtotalsAmount['text'] = f"Ksh. {self.orderQueue.getTotals(): .2f}"
        self.taxAmount['text'] = f"Ksh. {self.orderQueue.getTax(): .2f}"
        self.payableAmount['text'] = f"Ksh. {self.orderQueue.getTotals(): .2f}"
        self.orderQuantityValues['text'] = f"{self.orderQueue.getQuantity()}"

    def clearOrders(self) -> None:
        # Delete Treeview Child Elements
        if len(self.orderQueue) > 0:
            self.orderQueue.clearOrders("Normal")

        # Disable the print button
        self.printButton['state'] = tkinter.DISABLED
        self.holdButton['state'] = tkinter.DISABLED
        self.clearOrderBtn['state'] = tkinter.DISABLED
        self.cashInput['state'] = tkinter.DISABLED
        self.mpesaInput['state'] = tkinter.DISABLED

        self.resetTotals()

    def updateProgressBar(self, url):
        while True:
            # Time order fetching request
            try:
                req = requests.get(url)
                if req.status_code == 200:
                    break
            except:
                self.update_idletasks()
                self.progressBar['value'] += 10
                time.sleep(0.001)

    def loadStatus(self):
        self.searchImage = Image.open('icons/search.png').resize((18, 18), resample=Image.LANCZOS)
        self.searchIcon = ImageTk.PhotoImage(self.searchImage)

        self.searchBtn= tkinter.Button(self.statusBar, command=self.searchMenu, compound=tkinter.LEFT, image=self.searchIcon, relief=tkinter.GROOVE, text="Search", width=10)
        self.searchBtn.grid(column=0, row=0, ipady=1, ipadx=30)

        # Fill details of the Logged in Staff
        self.loggedInUser = tkinter.Button(self.statusBar, compound=tkinter.LEFT, relief=tkinter.GROOVE, text=STAFF, width=19)
        self.loggedInUser.grid(column=1, row=0, ipady=1)

        # Display the loaded data size
        self.dataButtton = tkinter.Button(self.statusBar, relief=tkinter.GROOVE, text="0.00KB", width=10)
        self.dataButtton.grid(column=2, row=0, ipady=1, ipadx=10) 

        # Show network fetching progress

        self.progressBar = ttk.Progressbar(self.statusBar, orient=tkinter.HORIZONTAL, length=280, mode="indeterminate")
        self.progressBar.grid(column=3, row=0, ipady=2.499)     

        # Indicate the Date & Time
        self.clockImage = Image.open('icons/clock.png').resize((18, 18), resample=Image.LANCZOS)
        self.clockIcon = ImageTk.PhotoImage(self.clockImage)

        self.loggedInUser = tkinter.Button(self.statusBar, compound=tkinter.LEFT, image=self.clockIcon, relief=tkinter.GROOVE, text=f"{datetime.datetime.today()}")
        self.loggedInUser.grid(column=4, row=0, ipady=1, ipadx=10)

        self.connectedImage = Image.open('icons/connected.png').resize((18, 18), resample=Image.LANCZOS)
        self.connectedIcon = ImageTk.PhotoImage(self.connectedImage)

        self.lConnectedUser = tkinter.Button(self.statusBar, compound=tkinter.LEFT, image=self.connectedIcon, relief=tkinter.GROOVE, text=f"Connected")
        self.lConnectedUser.grid(column=5, row=0, ipady=1, ipadx=10)

        self.alertImage = Image.open('icons/bell.png').resize((18, 18), resample=Image.LANCZOS)
        self.alertIcon = ImageTk.PhotoImage(self.alertImage)

        self.alertBtn = tkinter.Button(self.statusBar, compound=tkinter.LEFT, image=self.alertIcon, relief=tkinter.GROOVE, text=f"Notifications")
        self.alertBtn.grid(column=6, row=0, ipady=1, ipadx=10)

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
        self.clientOrderTree.column("Date", width=80)
        self.clientOrderTree.heading("Quantity", text="Quantity")
        self.clientOrderTree.column("Quantity", width=80)
        self.clientOrderTree.heading("Amount", text="Amount")
        self.clientOrderTree.column("Amount", width=80)
        self.clientOrderTree.heading("Status", text="Status")
        self.clientOrderTree.column("Status", width=80)
        self.clientOrderTree.heading("Payment", text="Payment")
        self.clientOrderTree.column("Payment", width=80)
        self.clientOrderTree.heading("Id", text="Id")
        self.clientOrderTree.column("Id", width=80)
        self.clientOrderTree.grid(padx=10)

        # Fetch the orders
        self.clientOrders = requests.get(f"https://{CLIENT_IP}/orders?business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN})
        if self.clientOrders.status_code == 200:
            # Add orders to the treeview
            for orders in self.clientOrders.json()['orders']:
                    self.clientOrderTree.insert("", tkinter.END, values=(orders['date'],
                        orders['id'],
                        sum([item['quantity'] for item in orders['ordered_item']]),
                        sum([item['price'] * item['quantity'] for item in orders['ordered_item']]),
                        orders['status'],
                        orders['payment_status']
                    )
                )
        else:
            messagebox.showerror("Error Fetching orders", "There seems to be an error fetching the products please contact the adminstrator")

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
        self.orderedQueueTree.column("Date", width=97)
        self.orderedQueueTree.heading("Table no.", text="Table no.")
        self.orderedQueueTree.column("Table no.", width=97)
        self.orderedQueueTree.heading("Served By", text="Served By")
        self.orderedQueueTree.column("Served By", width=97)
        self.orderedQueueTree.heading("price", text="price")
        self.orderedQueueTree.column("price", width=92)
        self.orderedQueueTree.heading("phone_number", text="Phone Number")
        self.orderedQueueTree.column("phone_number", width=97)
        self.orderedQueueTree.grid(padx=10)

        ## Bind right click Event to toogle payment of the pending orders

        # iterate the pending Orders
        for orders in self.orderQueue.pendingOrders:
            self.orderedQueueTree.insert("", tkinter.END,
                values=(
                    orders.time, orders.table, orders.served_by,
                    orders.price, orders.phone_number
                )
            )

    def addItem(self, item_id):
        # Fetch the product with id
        self.req = requests.get(f"https://{CLIENT_IP}/products/{item_id}")    
        assert self.req.status_code == 200
        order_item =  self.req.json()
        # Add item to order Queue
        order = ProductQueueAbc(id=item_id, name=order_item['name'], price=order_item['price'])
        self.orderQueue.addOrder(order)
        self.reloadOrderTreeView()

        # Change State of the print Button
        self.printButton['state'] = tkinter.NORMAL
        self.holdButton['state'] = tkinter.NORMAL
        self.clearOrderBtn['state'] = tkinter.NORMAL
        self.cashInput['state'] = tkinter.NORMAL
        self.mpesaInput['state'] = tkinter.NORMAL

        self.updateProgressBar(f"https://{CLIENT_IP}/products/{item_id}")

    def reloadOrderTreeView(self):
        self.orderTreeview.delete(*self.orderTreeview.get_children())
        for items in self.orderQueue.normalOrders:
            if items:
                self.orderTreeview.insert("", tkinter.END, values=(items.name, items.quantity, items.price))

        # Update the totals
        self.resetTotals()

    def preparePayment(self):
        if self.paymentVar.get() == 1:
            # Toggle Key pad Entry
            for widgets in self.ordersTreeviewFrame.winfo_children():
                widgets.destroy()

            self.calculator = CalcFrame(self.ordersTreeviewFrame)
            self.calculator.grid()
        else:
            # Show the normal counter button
            self.loadEntries()
        
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

            # self.eval("tk::PlaceWindow . Center")
            self.promptButton = tkinter.Button(self.clientWindow, text="Prompt Payment", command=self.promptMpesa, **self.buttonConfig)
            self.promptButton.grid(row=2, column=0)

    def toogleKeyboard(self, event):
        self.keyboard = Keyboard(self, event.widget)
        self.keyboard.place(x=16, y=550)

    def deleteKeyBoard(self, event):
        self.keyboard.destroy()

    def loadCustomer(self):
        pass

    def loadEntries(self):
        self.orderTreeview = ttk.Treeview(self.ordersTreeviewFrame,
            style="Treeview",
            show="headings",
            height=23,
            columns=("Name", "Quantity", "Amount"),
        )
        self.orderTreeview.heading("Name", text="Name")
        self.orderTreeview.column("Name", width=135)
        self.orderTreeview.heading("Quantity", text="Quantity")
        self.orderTreeview.column("Quantity", width=135)
        self.orderTreeview.heading("Amount", text="Amount")
        self.orderTreeview.column("Amount",width=135)
        self.orderTreeview.grid(row=0, column=0)

        # Check for items in the Queue
        for elements in self.orderQueue.normalOrders:
            if elements:
                self.orderTreeview.insert("", tkinter.END, values=(elements.name, elements.quantity, elements.price))
        # Bind Event to treeview
        self.orderTreeview.bind("<Button-3>", self.ManageOrders)

    def viewCustomer(self):
        for widgets in self.ordersTreeviewFrame.winfo_children():
            widgets.destroy()

        # Call the order tree view 
        self.loadEntries()

    def AddQueue(self):
        # Prompt for client Details
        self.queueWindow = tkinter.Toplevel()
        self.queueWindow.resizable((0,0))
        self.queueWindow.title("Queue Order")

        self.tableNumberLabel = tkinter.Label(self.queueWindow, text="Table No.")
        self.tableNumberLabel.grid(row=0, column=0, sticky=tkinter.W)

        self.tableNumber = tkinter.Entry(self.queueWindow)
        self.tableNumber.grid(row=1, column=0, padx=10, ipady=5, pady=5)

        self.customerPhoneLabel = tkinter.Label(self.queueWindow, text="Customer Phone.")
        self.customerPhoneLabel.grid(row=0, column=1, sticky=tkinter.W)

        self.customerPhone = tkinter.Entry(self.queueWindow)
        self.customerPhone.grid(row=1, column=1, padx=10, ipady=5, pady=5)

        self.customerNameLabel = tkinter.Label(self.queueWindow, text="Customer Name")
        self.customerNameLabel.grid(row=0, column=2, sticky=tkinter.W)

        self.customerName = tkinter.Entry(self.queueWindow)
        self.customerName.grid(row=1, column=2, padx=10, ipady=5, pady=5)

        self.submitReq = tkinter.Button(self.queueWindow, relief=tkinter.GROOVE, text="Queue Order", width=13, command=self.createPendingOrder)
        self.submitReq.grid(row=2, column=2, pady=5, ipady=5, ipadx=10)

    def createPendingOrder(self):
        self.orderQueue.addOrder(
            OrderedQueueAbc(**{
                "time": datetime.datetime.utcnow(),
                "price": self.orderQueue.getTotals(),
                "customer_name": self.customerName.get(),
                "served_by": STAFF,
                "table": self.tableNumber.get(),
                "phone_number": self.customerPhone.get()
            })
        )
        # Post order with status unpaid
        self.Orderpayload = {
            "id": self.order_id,
            "status": "incomplete",
            "business_id": CLIENT_BUSINESS['business'][0]["id"],
            "ordered_item": [
                    {
                        "quantity": item.quantity,
                        "price": item.price,
                        "order_id": self.order_id,
                        "product_id": self.getProductId(item.name)
                } for item in self.orderQueue.normalOrders if item
            ]
        }
        
        self.order = requests.post(f"https://{CLIENT_IP}/orders?business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN}, json=self.Orderpayload)

        if self.order.status_code == 200:
            # Pop the Item from the queue
            # Clear The normal orders
            self.orderQueue.clearOrders("Normal")
            self.queueWindow.destroy()
        else:
            messagebox.showerror("Order adding order", "Error order could not be created")

    def promptMpesa(self):
        # Pay for order -> Patch request to order class -> Post Request to Transactions class
        phone_number = self.phoneNumber.get()
        req = PAYMENT_SERVICE.collect.checkout(
                phone_number=phone_number,
                email="mutabletechke@gmail.com",
                amount=10,
                currency="KES",
                comment=""
            )
        return req

    def loadMenu(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

    def getProductId(self, name) -> str:
        # Add auth to headers
        req = requests.get(f"https://{CLIENT_IP}/products?name={name}&business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN})

        if req.status_code == 200:
            return req.json()['id']

    def printReceipt(self):
        """
            Validation for the Cash given
        """

        # Create order item and post to server
        # Loop over the queue item
        self.order_id = uuid.uuid4().hex
        self.completeOrderPayload = {
            "id": self.order_id,
            "status": "completed",
            "payment_mode": "Cash",
            "business_id": CLIENT_BUSINESS['business'][0]["id"],
            "ordered_item": [
                    {
                        "quantity": item.quantity,
                        "price": item.price,
                        "order_id": self.order_id,
                        "product_id": item.id
                } for item in self.orderQueue.normalOrders if item
            ]
        }

        self.orderRequest = requests.post(f"https://{CLIENT_IP}/orders?business_id={BUSINESS_ID}", headers={'Authorization': 'Bearer %s'%AUTH_TOKEN}, json=self.completeOrderPayload)

        if self.orderRequest.status_code == 201:
            self.orderQueue.printReceipt(
                BUSINESS_NAME,
                BUSINESS_PHONE,
                BUSINESS_LOCATION,
                self.calculator.getAmount(),
                STAFF
            )
            #  Clear The order from the queue
            self.clearOrders()
            self.viewCustomer()
        else:
            messagebox.showerror("Error generating receipt", "Error Printing receipt")

    def searchMenu(self):
        for widgets in self.midnav.winfo_children():
            widgets.destroy()

        self.inputFrame = tkinter.Frame(self.midnav)
        self.inputFrame.grid(row=0, column=0)

        self.searchFrame = tkinter.Entry(self.inputFrame, width=60)
        self.searchFrame.bind("<FocusIn>", self.toogleKeyboard)
        self.searchFrame.bind("<FocusOut>", self.deleteKeyBoard)
        self.searchFrame.grid(row=0, column=0, ipady=7)

        self.searchBtn = tkinter.Button(self.inputFrame, width=17, text="Search Food", relief=tkinter.GROOVE, command=self.filterProducts)
        self.searchBtn.grid(row=0, column=1, ipady=5, padx=3)

        self.searchResponseFrame = tkinter.Frame(self.midnav)
        self.searchResponseFrame.grid(row=1, column=0, padx=5)


        self.searchResponse = ttk.Treeview(self.searchResponseFrame,
            style="Treeview",
            show="headings",
            height=31,
            columns=("Name", "Out Of Stock", "Price"),
        )
        self.searchResponse.heading("Name", text="Name")
        self.searchResponse.column("Name", width=100)
        self.searchResponse.heading("Out Of Stock", text="Out Of Stock")
        self.searchResponse.column("Name", width=100)
        self.searchResponse.heading("Price", text="Price")
        self.searchResponse.column("Name", width=95)
        self.searchResponse.grid(row=0, column=0)


    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = Main()
    app.run()
