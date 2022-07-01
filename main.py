# First assumption we'll make: The file will have no header.
# Need to keep track of: 1) amount and its linked list 2) Order id
from collections import OrderedDict
from csv import reader

def readFile():
    # Key is the price
    # tuple to contain: ID, how many to buy/sell
    orderbook_ask = OrderedDict()
    orderbook_bid = OrderedDict()

    with open('TestData.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            if row[0] == 'A':
                if row[2] == 'S':
                    current_list = orderbook_ask.get(row[4], [()])
                    current_list.append((row[1], row[3]))
                    current_list = removeEmptyTuple(current_list)
                    orderbook_ask[row[4]] = current_list
                elif row[2] == 'B':
                    # We need to check for matching or lower prices now in the ask book

                    current_list = orderbook_bid.get(row[4], [()])
                    current_list.append((row[1], row[3]))
                    current_list = removeEmptyTuple(current_list)
                    orderbook_bid[row[4]] = current_list
            else:
                print("Remove new order:")
                print(row)
    print("hello")

def removeEmptyTuple(currentList):
    if currentList[0] == ():
        currentList = list(filter(None, currentList))
    return currentList


if __name__ == '__main__':
    readFile()


