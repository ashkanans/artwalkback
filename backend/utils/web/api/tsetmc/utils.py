def stock_info_to_list_dict(objects):
    result = []
    for obj in objects:
        item = {
            'tse_id': obj[0],
            'Company Name': obj[1],
            'Persian symbol': obj[2],
            'Industry Group': obj[3],
            'perc_final': obj[4],
            'perc_last': obj[5],
            'Value': obj[6],
            'Vol': obj[7],
            'market_cap': obj[8],
            'Final_price': obj[9],
            'first_price': obj[10],
            'last_price': obj[11],
            'Yesterday_price': obj[12],
            'Number_transactions': obj[13],
            'volume_ratio_to_month': obj[14],
            'buy_per_capita': obj[15],
            'sell_per_capita': obj[16],
            'entered_money': obj[17],
            'buyer_power': obj[18],
            'status': obj[19],
            'queue value': obj[20]
        }
        result.append(item)
    return result


def important_filters_to_list_dict(objects):
    result = []
    for obj in objects:
        item = {
            'tse_id_2': obj[0],
            'Persian_symbol': obj[1],
            'first_price': obj[2],
            'Final_price': obj[3],
            'last_price': obj[4],
            'Number_transactions': obj[5],
            'Vol': obj[6],
            'Value': obj[7],
            'Yesterday_price': obj[8],
            'per_change_price': obj[9],
            'status': obj[10],
            'queue_value': obj[11],
            'perc_last': obj[12],
            'volume_ratio_to_month': obj[13],
            'buy_per_capita': obj[14],
            'sell_per_capita': obj[15],
            'entered_money': obj[16],
            'buyer_power': obj[17]
        }
        result.append(item)
    return result


def commodity_to_list_dict(objects):
    price_history_dicts = []
    for obj in objects:
        price_history_dicts.append({
            'Close': obj.Close,
            'Date': obj.Date,
            'ID': obj.ID,
            'category': obj.category,
            'Name_en': obj.Name_en,
            'Unit': obj.Unit,
            'Name_fa': obj.Name_fa,
            'DateSh': obj.DateSh
        })
    return price_history_dicts
