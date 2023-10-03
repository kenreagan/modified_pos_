from collections import deque
import datetime
from typing import (
    Optional,
    Any,
    List,
    TypeVar
)
import win32print
import win32ui
import win32con
import ctypes
from ctypes import wintypes
from PIL import Image, ImageWin

class OrderedQueueAbc:
    def __init__(self, time: datetime.datetime, customer_name: str, served_by: str, table: int,
                 price: float,phone_number:str) -> None:
        self.time: datetime.datetime = time
        self.customer_name = customer_name
        self.served_by = served_by
        self.table = table
        self.price = price
        self.phone_number = phone_number
    
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(time={self.time!r}, customer_name={self.customer_name!r}, served_by={self.served_by!r}, table={self.table!r}, price={self.price!r}, phone={self.phone_no!r})'


class ProductQueueAbc:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f'{self.__class__.__qualname__}(name={self.name}, quantity={self.quantity}, price={self.price})'

T = TypeVar("T", OrderedQueueAbc, ProductQueueAbc)

class OrderQueue:
    def __init__(self):
        self.pendingOrders = deque()
        self.normalOrders = deque()
        self.defy: int = 4
        
    def addOrder(self, order: Optional[T]):
        # Check the instance of the order
        if isinstance(order, OrderedQueueAbc):
            for i in self.pendingOrders:
                if i.phone_number == order.phone_number:
                    i.price += order.price
                else:
                    self.pendingOrders.append(order)
        elif isinstance(order, ProductQueueAbc):
            if self.is_empty("Normal"):
                self.normalOrders.appendleft(order)
            else:
                for orders in self.normalOrders:
                    try:
                        if orders.name == order.name:
                            orders.quantity += order.quantity
                            order = None
                    except:
                        continue
                else:
                    self.normalOrders.append(order)
    
    def deleteOrder(self, order):
        if isinstance(order, OrderedQueueAbc):
            self.pendingOrders.remove(order)
        elif isinstance(order, ProductQueueAbc):
            self.normalOrders.remove(order)
    
    def find_order(self, category, name=None, phone_number: str=None):
        try:
            low, high = 0, len(self.pendingOrders) - 1 if category == "Pending" else len(self.normalOrders) - 1
            found_order = []
            while low <= high:
                mid = (low + high) // 2
                if category == "Pending":
                    if phone_number:
                        if self.pendingOrders[mid].phone_number == phone_number:
                            found_order.append(self.pendingOrders[mid])
                            left, right = mid - 1, mid + 1
                            while left >= 0 and self.pendingOrders[left].phone_number == phone_number:
                                found_order.append(self.pendingOrders[left])
                                left -= 1
                            while right < len(self.pendingOrders) and self.pendingOrders[right].phone_number == phone_number:
                                found_order.append(self.pendingOrders[right])
                                right += 1
                            return found_order
                        elif self.pendingOrders[mid].phone_number < phone_number:
                            low = mid + 1
                        else:
                            high = mid - 1
                else:
                    if name:
                        if self.normalOrders[mid].name == name:
                            found_order.append(self.normalOrders[mid])
                            left, right = mid - 1, mid + 1
                            while left >= 0 and self.normalOrders[left].name == name:
                                found_order.append(self.normalOrders[left])
                                left -= 1
                            while right < len(self.normalOrders) and self.normalOrders[right].phone_number == phone_number:
                                found_order.append(self.normalOrders[right])
                                right += 1
                            return found_order
                        elif self.normalOrders[mid].name < name:
                            low = mid + 1
                        else:
                            high = mid - 1
                    raise ValueError("Order identifier missing")
            return found_order
        
        except Exception as e:
            print(f"An error occurred while finding the order: {e}")

    def getTotals(self) -> float:
        return float(sum([(item.quantity * item.price) for item in self.normalOrders if item]))


    def getQuantity(self) -> float:
        return sum([item.quantity for item in self.normalOrders if item])

    def getTax(self):
        return 0.16 * self.getTotals()            

    def find_orders_by_time(self, start_time: datetime.datetime, end_time: datetime.datetime):
        try:
            return [order for order in self.pendingOrders if start_time <= order.time <= end_time]
        except Exception as e:
            print(f"An error occurred while finding the order by time: {e}")
 

    def clearOrders(self, category):
        try:
            self.pendingOrders.clear() if category == "Pending" else self.normalOrders.clear()
        except Exception as e:
            print(f"An error occurred while clearing orders: {e}")    

    def listOrders(self, category: str):
        try:
           return list(self.normalOrders) if category == "Normal" else list(self.pendingOrders)
        except Exception as e:
            print(f"An error occurred while listing orders: {e}")
 
    def is_empty(self, category) -> bool:
        try:
            return len(self.normalOrders) == 0 if category == "Normal" else len(self.pendingOrders)
        except Exception as e:
            print(f"An error occurred while checking whether order is empty: {e}")
            
    
    def __len__(self) -> int:
        return len(self.normalOrders)

    def draw_img(self, hdc, dib, maxh, maxw):
        w, h = dib.size
        h = min(h, maxh)
        w = min(w, maxw)
        l = (maxw - w) // 2
        t = (maxh - h) // self.defy
        dib.draw(hdc, (l, t, l + w, t + h))

    def add_img(self, hdc, file_name, new_page=False):
        maxw = hdc.GetDeviceCaps(win32con.HORZRES)
        maxh = hdc.GetDeviceCaps(win32con.VERTRES)
        img = Image.open(file_name).resize((220, 220), resample=Image.LANCZOS)
        dib = ImageWin.Dib(img)
        self.draw_img(hdc.GetHandleOutput(), dib, maxh, maxw)

    def padString(self, order) -> str:
        maxLen = max([len(item.name) for item in self.normalOrders])

        if len(order.name) < maxlen:
            outPut = str(order.name) + ' ' * maxLen - len(order)
            return outPut
        else:
            return order.name

    def printReceipt(self, store_name, business_phone, business_location, amountGiven, staff):
        self.printer = win32print.GetDefaultPrinter()
        self.hprinter = win32print.OpenPrinter(self.printer)
        self.printer_info = win32print.GetPrinter(self.hprinter, 2)

        self.printer_dc = win32ui.CreateDC()
        self.printer_dc.CreatePrinterDC(self.printer)
        self.printer_dc.StartDoc('Receipt')
        self.printer_dc.StartPage()
        self.printer_dc.SetTextAlign(win32con.TA_NOUPDATECP)
        self.printer_dc.SetBkMode(win32con.TRANSPARENT)
        self.printer_dc.SelectObject(win32ui.CreateFont({
            "name": "Exort Light",
            "height": 24
        }))
        self.x, self.y = 0, 0  
        self.line_height = 40

        left_margin = 0
        right_margin = 0
        top_margin = 0
        bottom_margin = 0

        self.printer_dc.TextOut(180, -5, f"{store_name.upper()} RESTAURANT")
        self.y += self.line_height
        self.printer_dc.TextOut(200, self.y, f"{business_location}")
        self.y += self.line_height
        self.printer_dc.TextOut(180, self.y, f"PHONE: {business_phone}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, "DATE: {:<25} {:^25} {:<20}".format(datetime.datetime.now().strftime("%D"), "TIME:", datetime.datetime.now().strftime("%H:%m:%S")))
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"{'-'*100}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, "{:<15} {:>25} {:>30}".format("ITEM", "QUANTITY", "AMT"))
        self.y += self.line_height

        # Iterate Over the Orders
        for orders in self.normalOrders:
            try:
                if orders:
                    self.printer_dc.TextOut(self.x, self.y, f"{orders.name: <15} {orders.quantity: >20} { (orders.price * orders.quantity): >30}")
                    self.y += self.line_height
                    self.defy += len(self) // 8
                else:
                    continue
            except:
                continue

        self.printer_dc.TextOut(self.x, self.y, f"{'-'*100}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y,f"{'-'*100}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"TOTAL AMOUNT: {self.getTotals(): .2f}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"TOTAL QUANTITY: {self.getQuantity()}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"AMOUNT PAID: {amountGiven: .2f}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"BALANCE: {float(amountGiven) - self.getTotals(): .2f}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"VAT TAX:  {self.getTax(): .2f}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"SERVED BY: {staff.upper()}")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"{'='*80}")
        self.y += self.line_height
        # Load image
        # self.add_img(self.printer_dc, "images/mutabletechpos.png")
        self.printer_dc.TextOut(self.x, self.y, "system by mutable tech: info@mutabletech.co.ke")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, "visit us on mutabletech.co.ke")
        self.y += self.line_height
        self.printer_dc.TextOut(self.x, self.y, f"{'='*80}")
        self.printer_dc.EndPage()
        self.printer_dc.EndDoc()
        self.printer_dc.DeleteDC()
