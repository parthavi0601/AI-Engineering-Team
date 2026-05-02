import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    
    def setUp(self):
        self.account = Account(account_number='12345', initial_deposit=10000)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 10000)

    def test_deposit(self):
        self.account.deposit(2000)
        self.assertEqual(self.account.balance, 12000)

    def test_withdraw(self):
        self.account.withdraw(5000)
        self.assertEqual(self.account.balance, 5000)

    def test_withdraw_insufficient_funds(self):
        initial_balance = self.account.balance
        self.account.withdraw(15000)
        self.assertEqual(self.account.balance, initial_balance)

    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.balance, 10000 - (150.0 * 5))
        self.assertEqual(self.account.holdings['AAPL'], 5)

    def test_buy_shares_insufficient_funds(self):
        self.account.withdraw(9000)  # Now balance = 1000
        self.account.buy_shares('TSLA', 2)
        self.assertEqual(self.account.balance, 1000)
        self.assertNotIn('TSLA', self.account.holdings)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 2)
        self.assertEqual(self.account.holdings['AAPL'], 3)
        self.assertEqual(self.account.balance, 10000 - (150.0 * 5) + (150.0 * 2))

    def test_sell_shares_insufficient_owned(self):
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 6)
        self.assertEqual(self.account.holdings['AAPL'], 5)  # No shares sold

    def test_total_portfolio_value(self):
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.total_portfolio_value(), self.account.balance + (150.0 * 5))

    def test_profit_loss(self):
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.profit_loss(), self.account.total_portfolio_value() - 10000)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 5})

    def test_get_transactions(self):
        self.account.buy_shares('AAPL', 5)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'buy')

if __name__ == '__main__':
    unittest.main()