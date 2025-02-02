from liquidity_pool import LiquidityPool
from wallet import Wallet

class InsurePool:
    def __init__(self, lp: LiquidityPool):
        self.lp = lp
        self.buyers = []  # Stores [wallet_address, amount_base, insurance_base]

    def buy(self, wallet: Wallet, amount_base: float, insurance_base: float) -> float:
        if amount_base > wallet.base:
            raise ValueError("Not enough base in the wallet.")

        # sell the base and get the asset
        asset_out = self.lp.buy(amount_base)

        # update wallet balances
        wallet.base -= (amount_base + insurance_base)
        wallet.asset += asset_out

        # if buying insurance add the buyer to the list
        if insurance_base:
            self.buyers.append([wallet.address, amount_base, insurance_base])

        return asset_out

    def sell(self, wallet: Wallet):

        amount_asset = wallet.asset

        if amount_asset > wallet.asset:
            raise ValueError("Not enough asset in the wallet.")

        # sell the asset and get the base
        base_out = self.lp.sell(amount_asset)

        # update wallet balances
        wallet.base += base_out
        wallet.asset -= amount_asset

        # find the seller in self.buyers and remove them
        for i, (address, initial_amount_base, insurance_base) in enumerate(self.buyers):
            if address == wallet.address:
                # remove the seller from the list
                self.buyers.pop(i)
                if base_out < initial_amount_base - insurance_base:
                    # if sold for loss return insurance to the seller
                    wallet.base += insurance_base
                    return base_out, insurance_base
                else:
                    # if sold for profit, distribute insurance to previous buyers
                    self._distribute_insurance(insurance_base)
                break

        return base_out, 0  

    def _distribute_insurance(self, insurance_base: float):
        # get the sum of insurance of all insurance holders
        total_prior_insurance = sum(b[2] for b in self.buyers)

        if total_prior_insurance == 0:
            return

        for i in range(len(self.buyers)):
            # distribute proportionally to all insurance holders
            proportion = self.buyers[i][2] / total_prior_insurance
            self.buyers[i][2] += proportion * insurance_base

    def get_asset_price(self) -> float:
        return self.lp.get_price()