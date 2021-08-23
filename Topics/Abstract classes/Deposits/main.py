from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, starting_sum, interest=None):
        self.sum = starting_sum
        self.interest = interest

    @abstractmethod
    def add_money(self, amount):
        ...

    def add_interest(self):
        ...


# create SavingsAccount and Deposit
class SavingsAccount(Account):
    def add_money(self, amount):
        if amount > 10:
            self.sum += amount
        else:
            print("Cannot add to SavingsAccount: amount too low.")


class Deposit(Account):
    def add_money(self, amount):
        if amount > 50:
            self.sum += amount
        else:
            print("Cannot add to Deposit: amount too low.")

    def add_interest(self):
        self.sum += self.sum * self.interest
