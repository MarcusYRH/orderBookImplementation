def order_book():
    import pandas as pd
    df = pd.read_csv("TestData2.csv", header=None,
                     names=["order_type", "order_id", "buy_or_sell", "number_of_shares", "price"])
    df['added']  = 'false'
    df['fulfilled'] = 'false'
    # df.loc[0, 'added'] = 'true'
    # df.loc[1, 'added'] = 'true'
    # df.loc[3, 'added'] = 'true'

    orders_made = []

    print(df)

    for row in df.itertuples():
        if row.order_type == 'A':
            if row.buy_or_sell == 'B':
                matching_sell_orders = df.loc[(df['price'] <= row.price) & df['added'].str.contains('true') & df['buy_or_sell'].str.contains('S')]
                number_outstanding = row.number_of_shares
                while not matching_sell_orders.empty:
                    max_sell_price_currently = df.loc[matching_sell_orders['price'].idxmax()]
                    fulfilled_sell_bool = max_sell_price_currently.number_of_shares - row.number_of_shares <= 0
                    df.loc[matching_sell_orders[
                               'price'].idxmax(), 'number_of_shares'] = 0 if fulfilled_sell_bool else max_sell_price_currently.number_of_shares - number_outstanding
                    df.loc[matching_sell_orders['price'].idxmax(), 'fulfilled'] = 'true' if fulfilled_sell_bool else 'false'
                    matching_sell_orders.loc[matching_sell_orders['price'].idxmax(), 'fulfilled'] = 'true' if fulfilled_sell_bool else 'false'

                    fulfilled_buy_bool = number_outstanding - max_sell_price_currently.number_of_shares <= 0
                    df.at[
                        row.Index, 'number_of_shares'] = 0 if fulfilled_buy_bool else number_outstanding - max_sell_price_currently.number_of_shares
                    df.at[row.Index, 'fulfilled'] = 'true' if fulfilled_buy_bool else 'false'

                    number_outstanding = number_outstanding if number_outstanding - max_sell_price_currently.number_of_shares <= 0 else number_outstanding - max_sell_price_currently.number_of_shares

                    if fulfilled_sell_bool & fulfilled_buy_bool:
                        orders_made.append("Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                                           .format(max_sell_price_currently.order_id, max_sell_price_currently.number_of_shares, max_sell_price_currently.price, row.order_id, max_sell_price_currently.number_of_shares, row.price))
                    elif fulfilled_sell_bool:
                        orders_made.append(
                            "Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Partially Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                            .format(max_sell_price_currently.order_id, max_sell_price_currently.number_of_shares,
                                    max_sell_price_currently.price, row.order_id, max_sell_price_currently.number_of_shares, row.price))
                    elif fulfilled_buy_bool:
                        orders_made.append(
                            "Partially Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                                .format(max_sell_price_currently.order_id, number_outstanding,
                                        max_sell_price_currently.price, row.order_id, number_outstanding, row.price))

                    matching_sell_orders = matching_sell_orders[matching_sell_orders.fulfilled.str.contains('false')]
                    if fulfilled_buy_bool:
                        break

                df.at[row.Index, 'added'] = 'true'
                df = df[df.number_of_shares != 0]

            elif row.buy_or_sell == 'S':
                matching_buy_orders = df.loc[(df['price'] >= row.price) & df['added'].str.contains('true') & df['buy_or_sell'].str.contains('B')]
                number_outstanding_2 = row.number_of_shares
                while not matching_buy_orders.empty:
                    max_buy_price_currently = df.loc[matching_buy_orders['price'].idxmax()]

                    fulfilled_buy_bool_2 = max_buy_price_currently.number_of_shares - number_outstanding_2 <= 0
                    df.loc[matching_buy_orders[
                               'price'].idxmax(), 'number_of_shares'] = 0 if fulfilled_buy_bool_2 else max_buy_price_currently.number_of_shares - number_outstanding_2
                    df.loc[matching_buy_orders['price'].idxmax(), 'fulfilled'] = 'true' if fulfilled_buy_bool_2 else 'false'
                    matching_buy_orders.loc[matching_buy_orders['price'].idxmax(), 'fulfilled'] = 'true' if fulfilled_buy_bool_2 else 'false'

                    fulfilled_sell_bool_2 = number_outstanding_2 - max_buy_price_currently.number_of_shares <= 0
                    df.at[
                        row.Index, 'number_of_shares'] = 0 if fulfilled_sell_bool_2 else number_outstanding_2 - max_buy_price_currently.number_of_shares
                    df.at[row.Index, 'fulfilled'] = 'true' if fulfilled_sell_bool_2 else 'false'

                    number_outstanding_2 = number_outstanding_2 if number_outstanding_2 - max_buy_price_currently.number_of_shares <= 0 else number_outstanding_2 - max_buy_price_currently.number_of_shares

                    if fulfilled_buy_bool_2 & fulfilled_sell_bool_2:
                        orders_made.append("Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                                           .format(row.order_id, max_buy_price_currently.number_of_shares, row.price, max_buy_price_currently.order_id, max_buy_price_currently.number_of_shares, max_buy_price_currently.price))
                    elif fulfilled_sell_bool_2:
                        orders_made.append(
                            "Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Partially Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                            .format(row.order_id, max_buy_price_currently.number_of_shares,
                                    row.price, max_buy_price_currently.order_id, max_buy_price_currently.number_of_shares, max_buy_price_currently.price))
                    elif fulfilled_buy_bool_2:
                        orders_made.append(
                            "Partially Fulfilled SELL order for SELL order ID: {}, SELL amount: {}, SELL price: {} || Fulfilled BUY order for BUY order ID: {}, BUY amount: {}, BUY price: {}"
                                .format(row.order_id, max_buy_price_currently.number_of_shares,
                                        row.price, max_buy_price_currently.order_id, max_buy_price_currently.number_of_shares, max_buy_price_currently.price))

                    matching_buy_orders = matching_buy_orders[matching_buy_orders.fulfilled.str.contains('false')]
                    if fulfilled_sell_bool_2:
                        break

                df.at[row.Index, 'added'] = 'true'
                df = df[df.number_of_shares != 0]
        else:
            df = df[df.order_id != row.order_id]
    print(df)
    print("Done!")

if __name__ == '__main__':
    order_book()