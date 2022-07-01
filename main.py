# First assumption we'll make: The file will have no header.
# Need to keep track of: 1) amount and its linked list 2) Order id
from collections import OrderedDict
from csv import reader


def read_file_pandas():
    import pandas as pd
    order_df = pd.read_csv("TestData.csv", header=None)
    print(order_df.to_string())


def read_file():
    import copy
    # Key is the price
    # tuple to contain: ID, how many to buy/sell
    orderbook_ask = OrderedDict()
    orderbook_bid = OrderedDict()
    trades_logged = []

    with open('TestData.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            price = int(row[4])
            order_type = row[0]
            buy_or_sell_type = row[2]
            order_id = int(row[1])
            trade_counter = 0
            if order_type == 'A':
                number_to_add = int(row[3])
                if buy_or_sell_type == 'S':
                    current_list = orderbook_ask.get(price, [()])
                    current_list.append((order_id, number_to_add))
                    current_list = remove_empty_tuple(current_list)
                    orderbook_ask[price] = current_list
                elif buy_or_sell_type == 'B':
                    outstanding = int(row[3])
                    # We need to check for matching or lower prices now in the ask book
                    for amt in list(orderbook_ask):
                        if outstanding == 0:
                            break
                        if amt <= price:
                            while orderbook_ask.get(amt):
                                if trade_counter == 0:
                                    original_amount_copy = copy.deepcopy(orderbook_ask.get(amt)[0][1])
                                if outstanding == 0:
                                    trades_logged.append(
                                        "Executed sell order for {} shares at sell id {} at sell price {}, for buy id "
                                        "{} at buy price {}".format(
                                            original_amount_copy if orderbook_ask.get(amt)[0][1] == 0 else original_amount_copy - orderbook_ask.get(amt)[0][1],
                                            tuple_li[0], amt, order_id, price))
                                    break
                                tuple_li = list(orderbook_ask.get(amt)[0])
                                tuple_li[1] -= 1
                                trade_counter += 1
                                if tuple_li[1] == 0:
                                    trades_logged.append(
                                        "Executed sell order for {} shares at sell id {} at sell price {}, for buy id "
                                        "{} at buy price {}".format(
                                            original_amount_copy,
                                            tuple_li[0], amt, order_id, price))
                                    original_amount_copy = 0
                                    trade_counter = 0
                                    orderbook_ask.get(amt).pop(0)
                                else:
                                    orderbook_ask.get(amt)[0] = tuple(tuple_li)
                                outstanding -= 1
                        if len(orderbook_ask.get(amt)) == 0:
                            del orderbook_ask[amt]

                    if outstanding != 0:
                        current_list = orderbook_bid.get(price, [()])
                        current_list.append((order_id, outstanding))
                        current_list = remove_empty_tuple(current_list)
                        orderbook_bid[price] = current_list

            else:
                if buy_or_sell_type == 'S':
                    for amt in list(orderbook_ask):
                        if amt == price:
                            tuples_list_for_price = orderbook_ask.get(amt)
                            # Usage of next is much faster than iterating whole list
                            tup = next(tup for tup in tuples_list_for_price if tup[0] == order_id)
                            orderbook_ask.get(amt).remove(tup)
                            break
                else:
                    for amt in list(orderbook_bid):
                        if amt == price:
                            tuples_list_for_price = orderbook_bid.get(amt)
                            # Usage of next is much faster than iterating whole list
                            tup = next(tup for tup in tuples_list_for_price if tup[0] == order_id)
                            orderbook_bid.get(amt).remove(tup)
                            if len(orderbook_bid.get(amt)) == 0:
                                del orderbook_bid[amt]
                            break
    print("TRADES EXECUTED FOR INPUT FILE:")
    for str in trades_logged:
        print(str)
    print("")
    print("ORDER BOOK FINAL STATE:")
    print("=================")
    print("ASK")
    for key in orderbook_ask:
        amounts_list = [i[1] for i in orderbook_ask.get(key)]
        print("{}: {}".format(key, amounts_list))
    print("------------")
    for key in orderbook_bid:
        amounts_list = [i[1] for i in orderbook_bid.get(key)]
        print("{}: {}".format(key, amounts_list))
    print("BID")

def remove_empty_tuple(current_list):
    if current_list[0] == ():
        current_list = list(filter(None, current_list))
    return current_list


if __name__ == '__main__':
    read_file()


