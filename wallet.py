class Wallet:
    def __init__(self, address: str, base: float):
        self.address = address
        self.base = base
        self.asset = 0
    
    def print_balances(self):
        print(f"Wallet {self.address} has {round(self.base, 2)} base and {round(self.asset, 2)} asset.")