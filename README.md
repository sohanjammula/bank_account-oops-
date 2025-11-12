# Banking System in Python

This project is a simple banking system implemented in Python following object-oriented programming principles. It supports multiple account types, transaction tracking, and encapsulation.

## Features

- **BankAccount base class:** Common functionality like deposit, withdrawal, transaction history, and statement printing.
- **SavingsAccount:** Supports interest calculation with a minimum balance restriction to protect the account.
- **CheckingAccount:** Supports overdraft protection with limits and fees.
- **Transaction tracking:** All transactions (deposits, withdrawals, fees, interest) are recorded with timestamps.
- **Encapsulation:** Sensitive account information is private and accessed only through public methods or properties.

## Technologies

- Python 3.x
- Uses standard libraries: `datetime`, `enum`, `typing`

## Usage

Run the script directly to see a demonstration of account creation, deposits, withdrawals, interest application, and statements:


## Classes

- **TransactionType:** Enum class defining transaction types.
- **Transaction:** Represents individual transactions.
- **BankAccount:** Abstracts general bank account operations.
- **SavingsAccount:** Extends BankAccount with interest and minimum balance constraints.
- **CheckingAccount:** Extends BankAccount with overdraft capabilities and fees.

## How to Extend

- Add new account types by subclassing `BankAccount`.
- Enhance transaction types or add transfer functionality.
- Integrate persistence with a database or file system.
- Add user authentication and multi-user support.

This repo is perfect for learning OOP concepts like encapsulation, inheritance, and polymorphism in Python with a practical banking example.
