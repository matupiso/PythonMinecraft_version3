from settings import * 

class InventoryItem:
    def __init__(self, item_id, count):
        self.item_id = item_id if item_id else 0
        self.count = count


        
    def __repr__(self):
        return f"{self.count}n{self.item_id}"
    def copy(self):
        return InventoryItem(self.item_id, self.count)