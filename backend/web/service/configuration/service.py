from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.configuration.stock_table_columns import StockTableColumns


# Creating the SQLAlchemy engine



class ConfigurationService:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_stock_table_configurations_for_user(self, username):
        existing_user = self.session.query(StockTableColumns).filter_by(Username=username).first()

        if existing_user:
            return "User already exists in the table"

        else:
            new_user_config = StockTableColumns(
                Username=username,
                Persian_symbol=True,
                Company_Name=True,
                Final_price=True,
                Yesterday_price=True,
                Industry_Group=True,
                Number_transactions=True,
                perc_last=True,
                perc_final=True,
                first_price=True,
                last_price=True,
                Value=True,
                market_cap=True,
                Vol=True,
                volume_ratio_to_month=True,
                entered_money=True,
                buy_per_capita=True,
                sell_per_capita=True,
                buyer_power=True,
                queue_value=True,
                status=True
            )

            self.session.add(new_user_config)
            self.session.commit()

            return "User configuration inserted successfully"

    def update_stock_table_configurations_for_user(self, username, **kwargs):
        existing_user = self.session.query(StockTableColumns).filter_by(Username=username).first()

        if existing_user:
            for key, value in kwargs.items():
                if hasattr(existing_user, key):
                    setattr(existing_user, key, value)

            self.session.commit()

            return "User configuration updated successfully"
        else:
            return "User does not exist in the table"

    def get_stock_table_configurations_for_user(self, username):
        user_config = self.session.query(StockTableColumns).filter_by(Username=username).first()

        if user_config:
            config_dict = {column.name: getattr(user_config, column.name) for column in user_config.__table__.columns}
            return config_dict
        else:
            return "User does not exist in the table"
