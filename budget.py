from typing import List
from itertools import zip_longest

class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []


    def deposit(self, amount: float, description: str = '', ledger = None) -> None:
        '''
        Creates a deposit record and adds it to the ledger in the form:
            {"amount": amount, "description": description}
        '''

        # Set to self.ledger if nothing is provided
        if ledger is None:
            ledger = self.ledger

        # Create and append object
        self.record_to_ledger(amount, description, ledger)


    def withdraw(self, amount: float, description: str = '', ledger = None) -> bool:
        '''
        Creates a withdrawal record and adds it to the ledger, given there is enough money in the ledger to complete the request. If this is successful it returns True, else False.
        '''

        # Set to self.ledger if nothing is provided
        if ledger is None:
            ledger = self.ledger

        # Checks the withdrawal from the category is possible
        if self.check_funds(amount) == False:
            return False

        # Add the record in the ledger
        self.record_to_ledger(float(-amount), description, ledger)
        return True


    def get_balance(self) -> int:
        '''
        Returns the current balance of the budget within this Category class, based on the net deposits and withdrawals.
        '''
        return sum([record['amount'] for record in self.ledger])


    def transfer(self, amount: float, budget_category: 'Category') -> bool:
        '''
        Creates a withdrawal record from one category, and adds it to another with a deposit record. This returns True if it was possible, otherwise False.
        '''
        # Return false if the requested amount is greater than the ledger balance
        if self.check_funds(amount) == False:
            return False

        # Withdraw the funds from ledger
        withdraw_description: str = f'Transfer to {budget_category.category}'
        self.withdraw(amount=amount,
                        description=withdraw_description,
                        ledger=self.ledger)

        # Add funds to the provided category
        deposit_description: str = f'Transfer from {self.category}'
        budget_category.deposit(amount=amount, 
                                description=deposit_description, 
                                ledger=budget_category.ledger)

        return True


    def check_funds(self, amount: float) -> bool:
        '''
        Returns true if the amount is less than the balance in the ledger, false otherwise.
        '''
        if amount > self.get_balance():
            return False

        return True

    @staticmethod
    def create_record(amount: float, description: str = ''):
        '''
        Creates an instance of the record object to be added to the ledger.
        '''
        return {"amount": amount, "description": description}

    def record_to_ledger(self, amount: float, description: str, ledger):
        '''
        Wraps the process for creating and appending a record to a provided ledger.
        '''
        record = self.create_record(amount, description)
        ledger.append(record)


    def __str__(self):
        '''
        Sets the display for the class when printed
        '''

        # Produce components of output
        name = self.category
        ledger = self.ledger
        header = name.center(30, '*') + '\n'
        items = [
            record['description'][:23].ljust(23) +
            f"{record['amount']:.2f}".rjust(7) + '\n' for record in ledger
        ]
        total = 'Total: ' + str(
            sum([record['amount'] for record in ledger]))

        # Construct output from components
        return str(f"{header}{''.join(items)}{total}")


f"*************Food*************\ndeposit                 900.00\nmilk, cereal, eggs, bac -45.67\nTransfer to Entertainme -20.00\nTotal: 834.33"



def create_spend_chart(categories: List['Category']):
    '''
    Given a list of up to 4 Category objects  that returns a bar chart string output. This will show the percentage spent in each category based on withdrawals, with 0 - 100 on the y-axis in increments of 10, and 'o' representing a single unit filling one of these increments. The x-axis will have the names of the categories vertically spelt, and a title at the top called 'Percentage spent by category'.

    An example of this:

       Percentage spent by category
       100|          
        90|          
        80|          
        70|          
        60| o        
        50| o        
        40| o        
        30| o        
        20| o  o     
        10| o  o  o  
         0| o  o  o  
           ----------
            F  C  A  
            o  l  u  
            o  o  t  
            d  t  o  
                h     
                i     
                n     
                g     
    '''
    # Title
    title: str = 'Percentage spent by category\n'
    # Construct axis
    y_axis: List[str] = [(str(x * 10) + '|').rjust(4) for x in range(0, 11)]

    # Construct x-axis
    number_of_categories = len(categories)
    x_axis = '    '  + (number_of_categories * 3 + 1) * '-' + '\n'

    # Construct titles
    category_names = [x.category for x in categories]
    y_axis_gap: str = '    '
    name_gap: str = '  '

    name_output: List[str] = []

    for k, name in enumerate(category_names):
        if k == 0:
            name_output.append([letter + name_gap for letter in name])
        else:
            name_output.append([letter + name_gap for letter in name])
    
    name_output = list(zip_longest(*name_output, fillvalue='   '))

    name_output = ''.join([y_axis_gap + ' ' + ''.join(list(x)) + ' \n' for x in name_output])[:-1] # Remove trailing newline

    # Construct data with name and amount within each object
    data = {
        obj.category: abs(sum([record['amount'] for record in obj.ledger if record['amount'] < 0]))
        for obj in categories
    }
    total_spend: int = sum([x for x in data.values()])
    data = {key: round((value / total_spend) * 100, -1) for key, value in data.items()}

    # For each level in the y-axis, produce a row
    body: List[str] = []
    bar_full: str = ' o '
    bar_empty: str = '   '

    for entry in range(0, 11):

        # Create a list for each row beginning with the y_axis value
        row: str = y_axis[entry]

        # For each category in the row
        for category in category_names:
            # If the amount is high enough, add to this row
            if data[category] >= entry * float(10):
                row += bar_full
            else:
                row += bar_empty

        body.append(row + ' \n')

    return title + ''.join(reversed(body)) + x_axis + name_output
