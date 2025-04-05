"""
Brain Wave Matrics Solution Task 1 Python
Create a fully functional ATM interface using Python
"""


# atm class
class ATM:
    def __init__(self, user_pin, initial_balance=0):
        self.user_pin = user_pin
        self.balance = initial_balance
# authenticate user
    def authenticate(self):
        attempts = 3
        while attempts > 0:
            entered_pin = input("Enter your 4-digit PIN: ")
            if entered_pin == self.user_pin:
                print("Login successful!\n")
                return True
            else:
                attempts -= 1
                print(f"Incorrect PIN. Attempts remaining: {attempts}")
        print("Too many failed attempts. Exiting.")
        return False
# ui menu
    def display_menu(self):
        print("\n--- ATM MENU ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")
# balance check
    def check_balance(self):
        print(f"Your current balance is: ₹{self.balance:.2f}")
# add deposit
    def deposit(self):
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            if amount <= 0:
                print("Enter a positive amount.")
                return
            self.balance += amount
            print(f"₹{amount:.2f} deposited successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
# withdraw
    def withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            if amount <= 0:
                print("Enter a positive amount.")
                return
            if amount > self.balance:
                print("Insufficient balance.")
                return
            self.balance -= amount
            print(f"₹{amount:.2f} withdrawn successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
# initiate
    def run(self):
        if not self.authenticate():
            return
        while True:
            self.display_menu()
            choice = input("Choose an option (1-4): ")
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

# test code
if __name__ == "__main__":
    atm = ATM(user_pin="1234", initial_balance=1000.00)
    atm.run()
