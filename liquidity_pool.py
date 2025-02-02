class LiquidityPool:
    def __init__(self, asset_reserve: float, base_reserve: float):
        self.asset_reserve = asset_reserve
        self.base_reserve = base_reserve
        self.k = asset_reserve * base_reserve

    def get_price(self) -> float:
        return self.base_reserve / self.asset_reserve
    
    def buy(self, amount_base: float) -> float:
        new_base_reserve = self.base_reserve + amount_base
        new_asset_reserve = self.k / new_base_reserve
        asset_out = self.asset_reserve - new_asset_reserve

        if asset_out <= 0:
            raise ValueError("Not enough liquidity in the pool.")
        
        self.base_reserve = new_base_reserve
        self.asset_reserve = new_asset_reserve
        return asset_out
    
    def sell(self, amount_asset: float) -> float:
        new_asset_reserve = self.asset_reserve + amount_asset
        new_base_reserve = self.k / new_asset_reserve
        base_out = self.base_reserve - new_base_reserve

        if base_out <= 0:
            raise ValueError("Not enough liquidity in the pool.")
    
        self.asset_reserve = new_asset_reserve
        self.base_reserve = new_base_reserve
        return base_out