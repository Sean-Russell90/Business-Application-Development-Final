"""Created by Sean Russell. 06.10.2020. Final_Project.py

A program that accepts input from the user pertaining to a book order. Stores the information in dictionaries and returns price, ship cost, number of books.
Input: Name, number of books ordered, prime and express status.    Output: Average revenue, total price, shipping cost, order counts, data stored in dictionaries.
"""

#globals
orders_dict = {} #dictionary which holds order number as the key and the class instance as the value
cust_dict = {} #dictionary which hold customer name as the key and order number as the value

#class

class Order:
    order_count = 0
    total_revenue = 0.0
    prime_count = 0
    express_count = 0

    #methods
    def __init__(self,name,num_books,prime,express,order_num):
        """Initializer class method"""
        self.name = name
        self.num_books = num_books
        self.prime = prime
        self.express = express
        self.order_num = order_num
        self.ship_cost = self.compute_express(express)
        self.price = self.compute_price(num_books)
        self.discount = self.compute_discount(prime,self.price)
        self.total_price = self.compute_total(self.ship_cost,self.discount,self.price)

    def compute_price(self,num_books):
        """Computes the price of the order. Input: number of books.  Output: price."""
        return num_books * 15

    def compute_discount(self,prime,price):
        """Computes the discount rate for the order.    Input: Prime status, price.  Output: discount rate."""
        if price < 150:
            return 0.5 if prime == True else False
        else:
            return 0.3 
    
    def compute_total(self,ship_cost,discount,price):
        """Computes the order total.    Input: ship cost, price, discount rate.  Output: total cost."""
        if discount:
            total_price = (price * discount) + ship_cost
        else:
            total_price = price + ship_cost

        return total_price

    def compute_express(self,express):
        """Computes the shipping cost.  Input: express status.  Output: ship cost."""
        return 5.0 if express == True else 0.0
    
    #output methods
    def save_txt(self):
        return f'{self.order_num:d}, {self.name:s}, {self.num_books:d}, {self.price:.2f}{self.ship_cost:.2f}'

    def __str__(self): 
        return f'Name: {self.name:^7s}|Order Number: {self.order_num:^7d}|Quantity: {self.num_books:^5d}|Price: ${self.total_price:^7.2f}|Ship Cost: ${self.ship_cost:^7.2f}\n'

    def __repr__(self): 
        return f'{self.name:^12s}|{self.order_num:^12d}|{self.num_books:^12d}|{self.total_price:^12.2f}|{self.ship_cost:^12.2f}'

    @classmethod
    def compute_average_revenue(cls):
        """Computes the average revenue using class variables."""
        if cls.order_count:
            avg = cls.total_revenue / cls.order_count
            return avg
        else:
            None

    @classmethod
    def summary(cls):
        """Display function used in the summary function outside of class."""
        avg = cls.compute_average_revenue()
        if avg is not None:
            return f'Order Count:\t\t{cls.order_count:d}\nPrime Count:\t\t{cls.prime_count:d}\nExpress Count:\t\t{cls.express_count:d}\nAverage Revenue:\t${avg:.2f}'
        else:
            return 'No data available.'

    @classmethod
    def reset(cls):
        """Resets all global dicts and class variables."""
        global cust_dict, orders_dict
        cls.order_count = 0
        cls.total_revenue = 0.0
        cls.prime_count = 0
        cls.express_count = 0
        orders_dict.clear()
        cust_dict.clear()

    @classmethod
    def delete(cls):
        """Method that takes input for an entry to delete, searches for it in this global dicts, and removes it."""
        global orders_dict

        if orders_dict:
            remove = int(input('Enter the order number to delete: -> '))

            for num in orders_dict:
                if num == remove:
                    cls.delete_from_cust_dict(remove)
                    del orders_dict[num]
                    return 'Order Deleted'
            else:
                'That number does not exist in the orders.'

        else:
            return 'No valid data to delete.'

    @classmethod
    def delete_from_cust_dict(cls,remove):
        """Method that removes an entry from the cust_dict dictionary."""
        global cust_dict

        remove = str(remove)

        for k,v in cust_dict.items():
            if v[0] == remove:
                del cust_dict[k]
                return

#functions

def submit():
    """Submit function accepts input from user, splits it into lists, initiliazes those inputs, and adds them to the class.
    Input: name, books ordered, prime and express status.    Output: order formatted with class formatting.
    """
    #accept and split inputs
    user_input = input('Enter customer name and number of books ordered (e.g. Sean 5) -> ')
    user_status = input('Enter (1/0) whether the customer is a prime member and if they ordered express shipping (e.g. 1 0) -> ')
    input_list = user_input.split()
    status_list = user_status.split()

    #initializations
    name = input_list[0]
    num_books = int(input_list[1])
    prime = int(status_list[0])
    express = int(status_list[1])
    order_num = assign_number()
    order = Order(name,num_books,prime,express,order_num)
    update_dicts(order.name,order,order.order_num)
    update_counts(order.name,order.prime,order.express,order.total_price)

    return print(order)
    
def update_counts(name,prime,express,price):
    """Updates the class counts to reflect the addition of new orders.
    Input: name, price, prime and express status.    Output: updated class variables.
    """
    if name:
        Order.order_count += 1
        Order.total_revenue += price

    if prime:
        Order.prime_count += 1
    
    if express:
        Order.express_count += 1

def assign_number():
    """Assigns an order number to each order."""
    global orders_dict
    order_num = 1000

    for num in orders_dict:
        if num in orders_dict:
            order_num += 1
    
    return order_num

def update_dicts(name,order,order_num):
    """Updates the global dictionaries with the order information from each order.
    Input: name, order(class instance), order number.    Output: updates global dictionaries.
    """
    global orders_dict, cust_dict

    orders_dict[order_num] = order

    order_num = str(order_num)

    if name not in cust_dict:
        cust_dict[name] = [order_num]
    else:
        cust_dict[name].append(order_num)

    return

def summary():
    """Calls the summary class method."""
    print(Order.summary())

def reset():
    """Accepts input and confirmation from the user about resetting values, then call class method reset."""
    confirm = int(input('Are you sure you want to clear the records? 1: Yes 0: No -> '))
    if confirm == True:
        print('The records have been cleared.')
        Order.reset()
    else:
        print('The records have NOT been cleared.')

def display():
    """Displays values of both global dictionaries."""
    global orders_dict, cust_dict
    if Order.order_count:
        short_line()
        print(f'{"Name":^10s}|{"Order Number(s)":^17s}')
        short_line()
        for name in cust_dict:
            order_num = cust_dict[name]
            print(f'{name:^10s}|{" ".join(str(x) for x in order_num):^17}')

        long_line()

        print(f'{"Name":^12s}|{"Order Num":^12s}|{"Quantity":^12s}|{"Price":^12s}|{"Ship Cost":^12s}')
        long_line()
        for num in orders_dict:
            order = orders_dict[num]
            print(order.__repr__())

    else:
        print('No valid data available.')
        return
    
def save():
    """Does not work, but would save the save the order info to a text file using a class output method."""
    file_name = input('Enter filename: -> ')

    with open(file_name,'w') as f:
        for x in orders_dict:
            f.write(x.save_txt() + '\n')

def load():
    """Does not work, but would accept and populate dictionaries with information from a text file."""
    global orders_dict
    inputfilename = input('Enter filename you wish to import: -> ')
    with open(inputfilename,'r') as f:
        lines = f.readlines()  
    
    for line in lines:
        inlist = line.split(',')  
        order = Order(inlist[0],inlist[1], inlist[2], inlist[3], inlist[4])
        orders_dict[inlist[0]] = [inlist[1], inlist[2], inlist[3], inlist[4]]

def search():
    """Iterates through the dictionaries to search for order number and returns the order information.
    Input: order number.    Output: dictionary value (order information).
    """
    global orders_dict

    if orders_dict:
        key = int(input('Enter the order number to search for: -> '))
        for number in orders_dict:
            if number == key:
                print(orders_dict[number])
                return
        else:
            print('Order number not found.')
    else:
        print('No valid data available.')

def search_by_name():
    """Iterates through the global dictionaries using the name as a search value rather than order number
    Input: name on order.   Output: order information.
    """
    global orders_dict, cust_dict

    if cust_dict:
        key = input('Enter the order name to search for: -> ')
        for name in cust_dict:
            if name == key:
                given = int(cust_dict[name][0])
                break

        for number in orders_dict:
            if number == given:
                print(orders_dict[number])
                return
        else:
            print('Order name not found.')
    else:
        print('No valid data available.')

def delete():
    """Calls the class method delete, which will delte an inputted and searched value from the global dictionaries."""
    print(Order.delete())

def short_line():
    """A short line to organize output with."""
    print('-' * 30)

def long_line():
    """A longer line to organize output with."""
    print('-' * 65)

#main

quit = False
while not quit :
    print ( '0.Load 1.Submit 2.Summary 3.Display 4.Search 5.Search by Name 6.Save 7.Delete 8.Reset 9.Exit' )
    choice = int ( input ( 'Enter your choice >> ' ))
    if choice == 0 :
        load()
    elif choice == 1 :
        submit()
    elif choice == 2 :
        summary()
    elif choice == 3 :
        display()
    elif choice == 4 :
        search()
    elif choice == 5:
        search_by_name()
    elif choice == 6 :
        save()
    elif choice == 7 :
        delete()
    elif choice == 8 :
        reset()
    elif choice == 9 :
        quit = True
    else :
        print ( 'Invalid input' )

print('Goodbye!')
