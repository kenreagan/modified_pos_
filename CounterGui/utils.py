from collections import deque
import datetime
from typing import Any,List

class OrderAbc:
    def __init__(self, time: datetime.datetime, customer_name: str, served_by: str, table: int,
                 price: float,phone_number:str) -> None:
        self.time: datetime.datetime = time
        self.customer_name = customer_name
        self.served_by = served_by
        self.table = table
        self.price = price
        self.phone_number=phone_number
        
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(time={self.time!r}, customer_name={self.customer_name!r}, served_by={self.served_by!r}, table={self.table!r}, price={self.price!r}, phone={self.phone_no!r})'


class OrderQueue:
    def __init__(self):
        self.orders = deque()
        
    
    def add_order(self, order: OrderAbc):
        try:
            existing_order =next((i for i in self.orders if i.phone_number == order.phone_number), None)
            if existing_order:
                existing_order.price += order.price
            else:
                self.orders.appendleft(order)
        
        except Exception as e:
            print(f"An error occurred while adding the order: {e}")
            
    
    def delete_order(self, order:OrderAbc):
        self.orders.remove(order)
    
    def find_order(self, phone_number: str) -> List[OrderAbc]:
        try:
            low, high = 0, len(self.orders) - 1
            found_order = []
            while low <= high:
                mid = (low + high) // 2
                if self.orders[mid].phone_number == phone_number:
                    found_order.append(self.orders[mid])
                    left, right = mid - 1, mid + 1
                    while left >= 0 and self.orders[left].phone_number == phone_number:
                        found_order.append(self.orders[left])
                        left -= 1
                    while right < len(self.orders) and self.orders[right].phone_number == phone_number:
                        found_order.append(self.orders[right])
                        right += 1
                    return found_order
                elif self.orders[mid].phone_number < phone_number:
                    low = mid + 1
                else:
                    high = mid - 1
            return found_order
        
        except Exception as e:
            print(f"An error occurred while finding the order: {e}")

    
    def get_total_revenue(self) -> float:
        try:
            return sum(order.price for order in self.orders)
        except Exception as e:
            print(f"An error occurred while getting total revenue: {e}")
            

    def find_orders_by_time(self, start_time: datetime.datetime, end_time: datetime.datetime) -> List[OrderAbc]:
        try:
            return [order for order in self.orders if start_time <= order.time <= end_time]
        except Exception as e:
            print(f"An error occurred while finding the order by time: {e}")
 

    def clear_orders(self):
        try:
            self.orders.clear()
        
        except Exception as e:
            print(f"An error occurred while clearing orders: {e}")
            

    def list_orders(self) -> List[OrderAbc]:
        try:
            return list(self.orders)
        except Exception as e:
            print(f"An error occurred while listing orders: {e}")
 
    def is_empty(self) -> bool:
        try:
            return len(self.orders) == 0
        except Exception as e:
            print(f"An error occurred while checking whether order is empty: {e}")
            
    
    def __len__(self) -> int:
        return len(self.orders)
        
