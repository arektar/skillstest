import pandas as pd

todt = lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')

def stat(orders, order_lines, top_num=10):
    most_pop_prod = pd.DataFrame()

    month_timedelta = pd.datetime.now() - pd.Timedelta(1, 'M')

    month_order_lines = order_lines[
        order_lines['OrderId'].isin(orders[orders['DateTime'] >= month_timedelta]['OrderId'])]
    most_pop_prod['ProductId'] = pd.DataFrame(month_order_lines['ProductId'].value_counts(sort=True, dropna=True)).head(
        top_num).index

    serching_orders = month_order_lines[month_order_lines['ProductId'].isin(most_pop_prod['ProductId'])]
    most_pop_prod = most_pop_prod.merge(serching_orders.loc[:, ['ProductId', 'Price']].groupby('ProductId',
                                                                                               as_index=False).sum(),
                                        left_on='ProductId', right_on='ProductId')
    most_pop_prod.rename(columns={'Price': 'TotalIncome'}, inplace=True)

    ord_price = serching_orders.loc[:, ['OrderId', 'Price']].groupby('OrderId', as_index=False).sum()
    ord_prod = serching_orders.loc[:, ['OrderId', 'ProductId']].drop_duplicates()
    ord_prod = ord_prod.merge(ord_price,
                              left_on='OrderId',
                              right_on='OrderId').groupby('ProductId',
                                                          as_index=False).mean().loc[:, ['ProductId', 'Price']]
    most_pop_prod = most_pop_prod.merge(ord_prod, left_on='ProductId', right_on='ProductId')
    most_pop_prod.rename(columns={'Price': 'AverageCheck'}, inplace=True)

    most_pop_prod=most_pop_prod.astype(dtype={'ProductId': 'int64',
                        'TotalIncome': 'float',
                        'AverageCheck': 'float'})

    return most_pop_prod


if __name__ == "__main__":
    orders = pd.DataFrame([
        [5, 583, todt('2017-01-01 15:03:17')],
        [13, 900, todt('2019-02-05 05:02:59')],
        [69, 19573, todt('2018-11-03 23:59:59')]],
        columns=['OrderId', 'CustomerId', 'DateTime']
    ).astype(dtype={'OrderId': 'int64', 'CustomerId': 'int64'})

    order_lines = pd.DataFrame([
        [5873, 5, 3026.0],
        [7265, 5, 573.0],
        [9675, 5, 159.0],
        [5873, 6, 2999.0],
        [13, 6, 57.0]],
        columns=['ProductId', 'OrderId', 'Price'],
    ).astype(dtype={'ProductId': 'int64', 'OrderId': 'int64', 'Price': 'float'})

    result = stat(orders, order_lines)
    print(result)
