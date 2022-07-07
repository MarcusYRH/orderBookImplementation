# # First assumption we'll make: The file will have no header.
# # Need to keep track of: 1) amount and its linked list 2) Order id
# from collections import OrderedDict
# from csv import reader
#
#
# def read_file_pandas():
#     import pandas as pd
#     df = pd.read_csv("test_case_2.csv", header=None,
#                      names=["order_type", "order_id", "buy_or_sell", "number_of_shares", "price"])
#     df = df.groupby(['order_type', 'price', 'buy_or_sell'], sort=False)[['number_of_shares', 'order_id']].agg(
#         list).reset_index()
#     print(df)
#     orderbook_sell = OrderedDict()
#     orderbook_buy = OrderedDict()
#
#     trades_done = []
#
#
#     for row in df.itertuples():
#         if row.order_type == 'A':
#             if row.buy_or_sell == 'S':
#                 sell_orders = list(zip(row.number_of_shares, row.order_id))
#                 orderbook_sell[row.price] = sell_orders
#                 matching_prices = [key for key in orderbook_buy if key >= row.price]
#                 if len(matching_prices) == 0:
#                     continue
#                 while sell_orders:  #Iterate thru each sell order since we found matching buy prices
#                     while matching_prices:
#                         matching_buy_orders = orderbook_buy.get(matching_prices[0])
#                         if not matching_buy_orders:
#                             del orderbook_buy[matching_prices[0]]
#                             matching_prices.pop(0)
#                             continue
#
#                         match_buy_order_tuple = matching_buy_orders[0]
#                         matching_buy_numbers = match_buy_order_tuple[0]
#                         matching_buy_id = match_buy_order_tuple[1]
#                         matching_buy_price = matching_prices[0]
#
#                         if sell_orders[0][0] - matching_buy_numbers >= 0:
#                             trades_done.append(
#                                 "Full trade execution: {} shares sold at sell price {} for sell order id {}; corresponding to buy order for {} shares bought at buy price {} buy order id {}"
#                                     .format(sell_orders[0][0], row.price, row.order_id, matching_buy_numbers,
#                                             matching_buy_price, matching_buy_id))
#                             if sell_orders[0][0] - matching_buy_numbers == 0:
#                                 sell_orders.pop(0)
#                             else:
#                                 match_buy_order_tuple_li = list(match_buy_order_tuple)
#                                 match_buy_order_tuple_li[0] -= matching_buy_numbers
#                                 matching_buy_orders[0] = tuple(match_buy_order_tuple_li)
#                             matching_buy_orders.pop(0)
#                         else:
#                             trades_done.append(
#                                 "Partial Trade execution: {} out of {} shares sold at sell price {} for sell order id {}; corresponding to buy order for {} shares bought at buy price {} buy order id {}"
#                                     .format(sell_orders[0][0], matching_buy_numbers, row.price, row.order_id,
#                                             matching_buy_numbers, matching_buy_price, matching_buy_id))
#                             match_buy_order_tuple_li = list(match_buy_order_tuple)
#                             match_buy_order_tuple_li[0] -= matching_buy_numbers
#                             matching_buy_orders[0] = tuple(match_buy_order_tuple_li)
#                             sell_orders.pop(0)
#
#             else:
#                 buy_orders = list(zip(row.number_of_shares, row.order_id))
#                 matching_prices = [key for key in orderbook_sell if key <= row.price]
#                 if len(matching_prices) == 0:
#                     orderbook_buy[row.price] = buy_orders
#                     continue
#                 while buy_orders:
#                     buy_order_original = buy_orders[0][0]
#                     buy_order_id = buy_orders[0][1]
#                     while matching_prices:  # Each matching sell price (with list of orders inside)
#                         matching_orders = orderbook_sell.get(matching_prices[0])
#                         if not matching_orders:
#                             del orderbook_sell[matching_prices[0]]
#                             matching_prices.pop(0)
#                             continue
#                         matching_order_tuple = matching_orders[0]
#                         matching_order_number = matching_order_tuple[0]
#                         matching_order_id = matching_order_tuple[1]
#                         if matching_order_number - buy_orders[0][0] >= 0:  # First matching sell order fully fulfil the first buy order
#                             trades_done.append("Full trade execution: {} shares sold at sell price {} for sell order id {}; corresponding to buy order for {} shares bought at buy price {} buy order id {}"
#                                                .format(buy_orders[0][0], matching_prices[0], matching_order_id, buy_order_original, row.price, buy_order_id))
#                             if matching_order_number - buy_orders[0][0] == 0:
#                                 matching_orders.pop(0)
#                             else:
#                                 matching_order_number -= buy_orders[0][0]
#                                 matching_order_tuple_li = list(matching_order_tuple)
#                                 matching_order_tuple_li[0] -= buy_orders[0][0]
#                                 matching_orders[0] = tuple(matching_order_tuple_li)
#                             buy_orders.pop(0)
#                             break
#                         else:
#                             trades_done.append(
#                                 "Partial Trade execution: {} out of {} shares sold at sell price {} for sell order id {}; corresponding to buy order for {} shares bought at buy price {} buy order id {}"
#                                 .format(matching_order_number, buy_orders[0][0], matching_prices[0], matching_order_id,
#                                         buy_orders[0][0], row.price, buy_order_id))
#                             buy_order_tuple_li = list(buy_orders[0])
#                             buy_order_tuple_li[0] -= matching_order_number
#                             buy_orders[0] = tuple(buy_order_tuple_li)
#                             matching_orders.pop(0)
#
#     print("hello")
#
#
#
# def read_file():
#     import copy
#     # Key is the price
#     # tuple to contain: ID, how many to buy/sell
#     orderbook_ask = OrderedDict()
#     orderbook_bid = OrderedDict()
#     trades_logged = []
#
#     with open('test_case_2.csv', 'r') as read_obj:
#         csv_reader = reader(read_obj)
#         for row in csv_reader:
#             # row variable is a list that represents a row in csv
#             price = int(row[4])
#             order_type = row[0]
#             buy_or_sell_type = row[2]
#             order_id = int(row[1])
#             trade_counter = 0
#             if order_type == 'A':
#                 number_to_add = int(row[3])
#                 if buy_or_sell_type == 'S':
#                     matching_prices = [key for key in orderbook_bid if key >= row.price]    # check in orderbook_bid for similar pricing
#                     for buy_price in matching_prices:
#                         if cleared_order:
#                             break
#                         cleared_order = False
#                         matching_orders = orderbook_bid.get(buy_price) # List of tuples returned
#                         while matching_orders:
#                             matching_order = matching_orders[0]
#                             matching_order_id = matching_order[0]
#                             matching_order_number = matching_order[1]
#                             if matching_order_number - number_to_add == 0:
#                                 matching_orders.pop(0) # Erase current order, move to next order
#                                 trades_logged.append(
#                                     "Executed sell order for {} shares at sell id {} at sell price {}, for buy id "
#                                     "{} at buy price {}".format(number_to_add, order_id, price, matching_order_id, buy_price))
#                                 cleared_order = True
#                                 break
#                             elif matching_order_number - number_to_add > 0:
#                                 matching_order_li = list(matching_order)  # Decrement existing buy order, continue to next record
#                                 matching_order_li[1] -= number_to_add
#                                 matching_order = tuple(matching_order_li)
#                                 matching_orders[0] = matching_order
#                                 cleared_order = True
#                                 break
#                             else:
#                     current_list = orderbook_ask.get(price, [()])
#                     current_list.append((order_id, number_to_add))
#                     current_list = remove_empty_tuple(current_list)
#                     orderbook_ask[price] = current_list
#                     orderbook_ask = OrderedDict(sorted(orderbook_ask.items(),reverse=True))
#
#                 elif buy_or_sell_type == 'B':
#                     outstanding = int(row[3])
#                     # Check if there's matching prices in the orderbook_bid
#                     # We need to check for matching or lower prices now in the ask book
#                     for amt in list(orderbook_ask):
#                         if outstanding == 0:
#                             break
#                         if amt <= price:
#                             while orderbook_ask.get(amt):
#                                 if trade_counter == 0:
#                                     original_amount_copy = copy.deepcopy(orderbook_ask.get(amt)[0][1])
#                                 if outstanding == 0:
#                                     trades_logged.append(
#                                         "Executed sell order for {} shares at sell id {} at sell price {}, for buy id "
#                                         "{} at buy price {}".format(
#                                             original_amount_copy if orderbook_ask.get(amt)[0][1] == 0 else original_amount_copy - orderbook_ask.get(amt)[0][1],
#                                             tuple_li[0], amt, order_id, price))
#                                     break
#                                 tuple_li = list(orderbook_ask.get(amt)[0])
#                                 tuple_li[1] -= 1
#                                 trade_counter += 1
#                                 if tuple_li[1] == 0:
#                                     trades_logged.append(
#                                         "Executed sell order for {} shares at sell id {} at sell price {}, for buy id "
#                                         "{} at buy price {}".format(
#                                             original_amount_copy,
#                                             tuple_li[0], amt, order_id, price))
#                                     original_amount_copy = 0
#                                     trade_counter = 0
#                                     orderbook_ask.get(amt).pop(0)
#                                 else:
#                                     orderbook_ask.get(amt)[0] = tuple(tuple_li)
#                                 outstanding -= 1
#                         if len(orderbook_ask.get(amt)) == 0:
#                             del orderbook_ask[amt]
#
#                     if outstanding != 0:
#                         current_list = orderbook_bid.get(price, [()])
#                         current_list.append((order_id, outstanding))
#                         current_list = remove_empty_tuple(current_list)
#                         orderbook_bid[price] = current_list
#                         orderbook_bid = OrderedDict(sorted(orderbook_bid.items(), reverse=True))
#             else:
#                 if buy_or_sell_type == 'S':
#                     for amt in list(orderbook_ask):
#                         if amt == price:
#                             tuples_list_for_price = orderbook_ask.get(amt)
#                             # Usage of next is much faster than iterating whole list
#                             tup = next((tup for tup in tuples_list_for_price if tup[0] == order_id), [])
#                             if tup:
#                                 orderbook_ask.get(amt).remove(tup)
#                             break
#                 else:
#                     for amt in list(orderbook_bid):
#                         if amt == price:
#                             tuples_list_for_price = orderbook_bid.get(amt)
#                             # Usage of next is much faster than iterating whole list
#                             tup = next(tup for tup in tuples_list_for_price if tup[0] == order_id)
#                             orderbook_bid.get(amt).remove(tup)
#                             if len(orderbook_bid.get(amt)) == 0:
#                                 del orderbook_bid[amt]
#                             break
#     print("TRADES EXECUTED FOR INPUT FILE:")
#     for str in trades_logged:
#         print(str)
#     print("")
#     print("ORDER BOOK FINAL STATE:")
#     print("=================")
#     print("ASK")
#     for key in orderbook_ask:
#         amounts_list = [i[1] for i in orderbook_ask.get(key)]
#         print("{}: {}".format(key, amounts_list))
#     print("------------")
#     for key in orderbook_bid:
#         amounts_list = [i[1] for i in orderbook_bid.get(key)]
#         print("{}: {}".format(key, amounts_list))
#     print("BID")
#
# def remove_empty_tuple(current_list):
#     if current_list[0] == ():
#         current_list = list(filter(None, current_list))
#     return current_list
#
#
# if __name__ == '__main__':
#     read_file()