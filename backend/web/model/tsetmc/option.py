from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Option(Base):
    __tablename__ = 'option'
    __table_args__ = {'schema': 'app'}

    tse_id = Column(String(255), nullable=True, primary_key=True)
    contractSize = Column(Integer, nullable=True)
    ua_tse_id = Column(String(255), nullable=True)
    ua_symbol = Column(String(255), nullable=True)
    ua_final_price = Column(Integer, nullable=True)
    ua_yesterday_price = Column(Integer, nullable=True)
    strikePrice = Column(Integer, nullable=True)
    remainedDay = Column(Integer, nullable=True)
    last_price = Column(Integer, nullable=True)
    open_position = Column(Integer, nullable=True)
    final_price = Column(Integer, nullable=True)
    yesterday_price = Column(Integer, nullable=True)
    notionalValue = Column(Float, nullable=True)
    value = Column(Float, nullable=True)
    vol = Column(Integer, nullable=True)
    tran_no = Column(Integer, nullable=True)
    symbol_desc = Column(String(255), nullable=True)
    symbol = Column(String(255), nullable=True)
    buy_price_first_line = Column(Integer, nullable=True)
    buy_vol_first_line = Column(Integer, nullable=True)
    sell_price_first_line = Column(Integer, nullable=True)
    sell_vol_first_line = Column(Integer, nullable=True)
    yesterday_open_position = Column(Integer, nullable=True)
    profit_status = Column(String(255), nullable=True)
    id = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    beginDate = Column(String(255), nullable=True)
    endDate = Column(String(255), nullable=True)
    Cost_of_Stock = Column(Float, nullable=True)
    amount_of_profit_or_loss = Column(Float, nullable=True)
    VOLATILITY12M = Column(Float, nullable=True)
    diff_Black_Scholes = Column(Integer, nullable=True)  # Adjusted name to avoid special character
    Expected_return_on_stocks = Column(Float, nullable=True)  # Adjusted name to avoid spaces
    Black_Scholes = Column(Float, nullable=True)  # Adjusted name to avoid special character
    VOLATILITY3M = Column(String(255), nullable=True)
    VOLATILITY6M = Column(String(255), nullable=True)
    delta = Column(String(255), nullable=True)
    IV = Column(String(255), nullable=True)
    leverage = Column(String(255), nullable=True)
    break_even = Column(String(255), nullable=True)  # Adjusted name to avoid spaces
    gap = Column(String(255), nullable=True)
    ua_final_price_change_perc = Column(Float, nullable=True)


def option_to_dict(option):
    if option[0].type == 'اختيار خريد':
        option_call = option[0]
        option_put = option[1]
    else:
        option_call = option[1]
        option_put = option[0]

    base_fields = [
        "contractSize", "ua_tse_id", "ua_symbol", "ua_final_price", "ua_yesterday_price",
        "strikePrice", "remainedDay", "beginDate", "endDate", "ua_final_price_change_perc"
    ]

    call_fields = [
        "tse_id", "last_price", "open_position", "final_price", "yesterday_price",
        "notionalValue", "value", "vol", "tran_no", "symbol_desc", "symbol",
        "buy_price_first_line", "buy_vol_first_line", "sell_price_first_line", "sell_vol_first_line",
        "yesterday_open_position", "profit_status", "Cost_of_Stock", "amount_of_profit_or_loss",
        "VOLATILITY12M", "diff_Black_Scholes", "Expected_return_on_stocks", "Black_Scholes",
        "VOLATILITY3M", "VOLATILITY6M", "delta", "IV", "leverage", "break_even", "gap"
    ]

    put_fields = call_fields

    result = {
        "id": option[0].id,
        "base": {field: getattr(option_put, field) for field in base_fields},
        "call": {field: getattr(option_call, field) for field in call_fields},
        "put": {field: getattr(option_put, field) for field in put_fields}
    }

    return result
