
def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)  # Return 0 if symbol not found


class Account:
    def __init__(self, account_number: str, initial_deposit: float) -> None:
        self.account_number = account_number
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount

    def buy_shares(self, symbol: str, quantity: int) -> None:
        price = get_share_price(symbol)
        if price * quantity > self.balance:
            print("Not enough funds for purchase.")
        else:
            self.balance -= (price * quantity)
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append({
                'type': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total': price * quantity
            })

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            print("User does not own enough shares of this symbol.")
        else:
            self.balance += (get_share_price(symbol) * quantity)
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({
                'type': 'sell',
                'symbol': symbol,
                'quantity': quantity,
                'price': get_share_price(symbol),
                'total': get_share_price(symbol) * quantity
            })

    def total_portfolio_value(self) -> float:
        return self.balance + sum(price * quantity for symbol, quantity in self.holdings.items() for price in [get_share_price(symbol)])

    def profit_loss(self) -> float:
        return self.total_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_profit_loss(self) -> float:
        return self.profit_loss()

    def get_transactions(self) -> list:
        return self.transactions


# Example usage of the Account class
account = Account(account_number='12345', initial_deposit=10000)
account.deposit(2000)
account.buy_shares('AAPL', 5)
account.sell_shares('TSLA', 2)
print(account.get_holdings())
print(account.profit_loss())
print(account.get_transactions())
