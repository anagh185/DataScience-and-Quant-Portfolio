import json

class Beverage:
    def __init__(self, name, size, price, stock):
        self.name = name
        self.size = size
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "price": self.price,
            "stock": self.stock
        }

    @staticmethod
    def from_dict(data):
        return Beverage(
            name=data["name"],
            size=data["size"],
            price=data["price"],
            stock=data["stock"]
        )

class Inventory:
    def __init__(self, filename="inventory.json"):
        self.filename = filename
        self.beverages = {}
        self.low_stock_threshold = 10
        self.load_inventory()
        self.prefill_inventory()

    def prefill_inventory(self):
        if not self.beverages:
            print("Prefilling inventory with default beverages...")
            default_beverages = [
                Beverage("Tea", "250ml", 1.50, 50),
                Beverage("Coffee", "250ml", 2.00, 50),
                Beverage("Coke", "330ml", 1.75, 30),
                Beverage("Pepsi", "330ml", 1.75, 30),
                Beverage("Sprite", "330ml", 1.75, 30)
            ]
            for beverage in default_beverages:
                self.beverages[beverage.name] = beverage

    def add_beverage(self, name, size, price, stock):
        if name in self.beverages:
            print(f"Beverage '{name}' already exists in the inventory.")
        else:
            self.beverages[name] = Beverage(name, size, price, stock)
            print(f"Beverage '{name}' added to the inventory.")

    def update_stock(self, name, amount):
        if name in self.beverages:
            self.beverages[name].stock += amount
            print(f"Stock for '{name}' updated. New stock: {self.beverages[name].stock}")
            if self.beverages[name].stock < self.low_stock_threshold:
                print(f"Warning: Stock for '{name}' is low! Consider placing an order.")
        else:
            print(f"Beverage '{name}' not found in the inventory.")

    def display_inventory(self):
        if not self.beverages:
            print("The inventory is empty.")
        else:
            print("\nCurrent Inventory:")
            for beverage in self.beverages.values():
                low_stock_indicator = " (LOW STOCK!)" if beverage.stock < self.low_stock_threshold else ""
                print(f"- {beverage.name} ({beverage.size}): ${beverage.price:.2f}, Stock: {beverage.stock}{low_stock_indicator}")

    def save_inventory(self):
        data = {name: beverage.to_dict() for name, beverage in self.beverages.items()}
        with open(self.filename, "w") as file:
            json.dump(data, file)
        print("Inventory saved to file.")

    def load_inventory(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.beverages = {name: Beverage.from_dict(details) for name, details in data.items()}
            print("Inventory loaded from file.")
        except FileNotFoundError:
            print("No existing inventory file found. Starting with an empty inventory.")
        except json.JSONDecodeError:
            print("Inventory file is corrupt. Starting with an empty inventory.")

# Main program logic
def main():
    inventory = Inventory()

    while True:
        print("\nInventory Management System")
        print("1. Add Beverage")
        print("2. Update Stock")
        print("3. Display Inventory")
        print("4. Save and Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter beverage name: ")
            size = input("Enter size (e.g., '500ml'): ")
            price = float(input("Enter price: "))
            stock = int(input("Enter initial stock: "))
            inventory.add_beverage(name, size, price, stock)
        elif choice == "2":
            name = input("Enter beverage name: ")
            amount = int(input("Enter stock change (positive to add, negative to remove): "))
            inventory.update_stock(name, amount)
        elif choice == "3":
            inventory.display_inventory()
        elif choice == "4":
            inventory.save_inventory()
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
