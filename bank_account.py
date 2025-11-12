from datetime import datetime
from typing import List, Dict
from enum import Enum

class TransactionType(Enum):
    """Enum for transaction types"""
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    INTEREST = "Interest"
    OVERDRAFT_FEE = "Overdraft Fee"
    TRANSFER = "Transfer"

class Transaction:
    """Represents a single transaction"""
    def __init__(self, trans_type: TransactionType, amount: float, balance_after: float, description: str = ""):
        self.__trans_type = trans_type
        self.__amount = amount
        self.__balance_after = balance_after
        self.__timestamp = datetime.now()
        self.__description = description
    
    def __str__(self):
        return (f"{self.__timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{self.__trans_type.value}: ${self.__amount:.2f} | "
                f"Balance: ${self.__balance_after:.2f} | "
                f"{self.__description}")
    
    @property
    def trans_type(self):
        return self.__trans_type
    
    @property
    def amount(self):
        return self.__amount
    
    @property
    def timestamp(self):
        return self.__timestamp

class BankAccount:
    """Base class for bank accounts with encapsulation and transaction tracking"""
    
    account_counter = 1000  # Class variable for generating account numbers
    
    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.__account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        
        self.__owner = owner
        self.__balance = initial_balance
        self.__transaction_history: List[Transaction] = []
        self.__is_active = True
        
        if initial_balance > 0:
            self.__add_transaction(TransactionType.DEPOSIT, initial_balance, "Initial deposit")
    
    def __add_transaction(self, trans_type: TransactionType, amount: float, description: str = ""):
        """Private method to add transaction to history"""
        transaction = Transaction(trans_type, amount, self.__balance, description)
        self.__transaction_history.append(transaction)
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into the account"""
        if not self.__is_active:
            print("Account is closed. Cannot perform transaction.")
            return False
        
        if amount <= 0:
            print("Deposit amount must be positive")
            return False
        
        self.__balance += amount
        self.__add_transaction(TransactionType.DEPOSIT, amount)
        print(f"Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account"""
        if not self.__is_active:
            print("Account is closed. Cannot perform transaction.")
            return False
        
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False
        
        if amount > self.__balance:
            print(f"Insufficient funds. Available balance: ${self.__balance:.2f}")
            return False
        
        self.__balance -= amount
        self.__add_transaction(TransactionType.WITHDRAWAL, amount)
        print(f"Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}")
        return True
    
    def get_balance(self) -> float:
        """Get current account balance"""
        return self.__balance
    
    def get_transaction_history(self, limit: int = None) -> List[Transaction]:
        """Get transaction history (most recent first)"""
        history = self.__transaction_history[::-1]
        return history[:limit] if limit else history
    
    def print_statement(self, num_transactions: int = 10):
        """Print account statement"""
        print(f"\n{'='*70}")
        print(f"Account Statement - {self.__class__.__name__}")
        print(f"{'='*70}")
        print(f"Account Number: {self.__account_number}")
        print(f"Owner: {self.__owner}")
        print(f"Current Balance: ${self.__balance:.2f}")
        print(f"Account Status: {'Active' if self.__is_active else 'Closed'}")
        print(f"\nRecent Transactions (Last {num_transactions}):")
        print(f"{'-'*70}")
        
        transactions = self.get_transaction_history(num_transactions)
        if transactions:
            for trans in transactions:
                print(trans)
        else:
            print("No transactions yet")
        print(f"{'='*70}\n")
    
    def close_account(self):
        """Close the account"""
        self.__is_active = False
        print(f"Account {self.__account_number} has been closed")
    
    # Getters for protected information
    @property
    def account_number(self):
        return self.__account_number
    
    @property
    def owner(self):
        return self.__owner
    
    @property
    def is_active(self):
        return self.__is_active
    
    def __str__(self):
        return f"{self.__class__.__name__}(#{self.__account_number}, Owner: {self.__owner}, Balance: ${self.__balance:.2f})"

class SavingsAccount(BankAccount):
    """Savings account with interest calculation"""
    
    def __init__(self, owner: str, initial_balance: float = 0.0, interest_rate: float = 0.02):
        super().__init__(owner, initial_balance)
        self.__interest_rate = interest_rate  # Annual interest rate (e.g., 0.02 = 2%)
        self.__minimum_balance = 100.0
    
    def apply_interest(self):
        """Apply interest to the account balance"""
        if not self.is_active:
            print("Account is closed. Cannot apply interest.")
            return False
        
        interest = self.get_balance() * self.__interest_rate
        if interest > 0:
            self._BankAccount__balance += interest
            self._BankAccount__add_transaction(
                TransactionType.INTEREST, 
                interest, 
                f"Interest at {self.__interest_rate*100:.2f}% rate"
            )
            print(f"Interest applied: ${interest:.2f}. New balance: ${self.get_balance():.2f}")
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        """Override withdraw to check minimum balance"""
        if not self.is_active:
            print("Account is closed. Cannot perform transaction.")
            return False
        
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False
        
        if self.get_balance() - amount < self.__minimum_balance:
            print(f"Withdrawal denied. Minimum balance of ${self.__minimum_balance:.2f} required.")
            return False
        
        return super().withdraw(amount)
    
    def set_interest_rate(self, new_rate: float):
        """Update interest rate"""
        if 0 <= new_rate <= 1:
            self.__interest_rate = new_rate
            print(f"Interest rate updated to {new_rate*100:.2f}%")
        else:
            print("Interest rate must be between 0 and 1 (0% - 100%)")
    
    @property
    def interest_rate(self):
        return self.__interest_rate

class CheckingAccount(BankAccount):
    """Checking account with overdraft protection"""
    
    def __init__(self, owner: str, initial_balance: float = 0.0, overdraft_limit: float = 500.0):
        super().__init__(owner, initial_balance)
        self.__overdraft_limit = overdraft_limit
        self.__overdraft_fee = 35.0
        self.__is_overdrawn = False
    
    def withdraw(self, amount: float) -> bool:
        """Override withdraw to allow overdraft"""
        if not self.is_active:
            print("Account is closed. Cannot perform transaction.")
            return False
        
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False
        
        available_funds = self.get_balance() + self.__overdraft_limit
        
        if amount > available_funds:
            print(f"Withdrawal denied. Exceeds overdraft limit.")
            print(f"Available: ${self.get_balance():.2f} + ${self.__overdraft_limit:.2f} overdraft")
            return False
        
        # Process withdrawal
        self._BankAccount__balance -= amount
        self._BankAccount__add_transaction(TransactionType.WITHDRAWAL, amount)
        
        # Check if overdrawn and apply fee
        if self.get_balance() < 0 and not self.__is_overdrawn:
            self.__is_overdrawn = True
            self._BankAccount__balance -= self.__overdraft_fee
            self._BankAccount__add_transaction(
                TransactionType.OVERDRAFT_FEE, 
                self.__overdraft_fee,
                "Overdraft fee charged"
            )
            print(f"⚠️  Withdrew ${amount:.2f}. Overdraft fee ${self.__overdraft_fee:.2f} applied.")
            print(f"   Current balance: ${self.get_balance():.2f}")
        else:
            print(f"Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}")
        
        # Reset overdrawn status if back to positive
        if self.get_balance() >= 0:
            self.__is_overdrawn = False
        
        return True
    
    def deposit(self, amount: float) -> bool:
        """Override deposit to reset overdraft status"""
        result = super().deposit(amount)
        if result and self.get_balance() >= 0:
            self.__is_overdrawn = False
        return result
    
    @property
    def overdraft_limit(self):
        return self.__overdraft_limit
    
    @property
    def is_overdrawn(self):
        return self.__is_overdrawn


# Demo Usage
if __name__ == "__main__":
    print("=== Banking System Demo ===\n")
    
    # Create accounts
    print("1. Creating accounts...")
    savings = SavingsAccount("Alice Johnson", 1000.0, interest_rate=0.03)
    checking = CheckingAccount("Bob Smith", 500.0, overdraft_limit=300.0)
    
    print(f"\n{savings}")
    print(f"{checking}\n")
    
    # Test savings account
    print("\n2. Testing Savings Account:")
    print("-" * 50)
    savings.deposit(500)
    savings.withdraw(200)
    savings.apply_interest()
    savings.withdraw(1200)  # Should fail (minimum balance)
    
    # Test checking account
    print("\n3. Testing Checking Account:")
    print("-" * 50)
    checking.deposit(200)
    checking.withdraw(600)  # Normal withdrawal
    checking.withdraw(150)  # Should trigger overdraft fee
    checking.deposit(100)
    
    # Print statements
    print("\n4. Account Statements:")
    savings.print_statement(5)
    checking.print_statement(5)
    
    # Demonstrate encapsulation
    print("\n5. Demonstrating Encapsulation:")
    print("-" * 50)
    print(f"Savings account number: {savings.account_number}")
    print(f"Checking account owner: {checking.owner}")
    print(f"Cannot directly access private __balance attribute")
    print(f"Use get_balance() instead: ${checking.get_balance():.2f}")