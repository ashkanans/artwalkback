import time
from collections import defaultdict
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.codal.letter import Letter
from backend.web.model.codal.letter_types import LetterType
from backend.web.model.codal.notification_configurations import NotificationConfiguration
from backend.web.model.codal.publisher import Publisher
from backend.web.model.codal.users_notification import UserNotification
from backend.web.model.ime.commodity_exchange_arzeh import CommodityExchangeArzeh
from backend.web.model.ime.commodity_exchange_export import CommodityExchangeExport
from backend.web.model.ime.commodity_exchange_physical import CommodityExchangePhysical
from backend.web.model.ime.sources import Sources


class CodalService:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update_notification_configuration(self, username, including=None, excluding=None,
                                          publisher_national_code=None, letter_types=None,
                                          period=None, lettersChecked=None, attachmentsChecked=None):
        # Query the existing configuration for the given username
        existing_config = self.session.query(NotificationConfiguration).filter_by(username=username).first()

        if not existing_config:
            raise ValueError("No notification configuration found for the provided username")

        # Update the fields if new values are provided
        if including is not None:
            existing_config.including = including
        if excluding is not None:
            existing_config.excluding = excluding
        if publisher_national_code is not None:
            existing_config.publisher_national_code = publisher_national_code
        if letter_types is not None:
            existing_config.letter_types = letter_types
        if period is not None:
            existing_config.period = period
        if lettersChecked is not None:
            existing_config.lettersChecked = lettersChecked
        if attachmentsChecked is not None:
            existing_config.attachmentsChecked = attachmentsChecked

        # Update the modification datetime
        existing_config.modified_datetime = datetime.now()

        # Commit the changes to the session
        self.session.commit()

    def add_notification_configuration(self, user_id, including, excluding, publisher_national_code, letter_types,
                                       period, lettersChecked, attachmentsChecked):

        new_config = NotificationConfiguration(
            user_id=user_id,
            including=including,
            excluding=excluding,
            publisher_national_code=publisher_national_code,
            letter_types=letter_types,
            period=period,
            lettersChecked=lettersChecked,
            attachmentsChecked=attachmentsChecked,
            created_datetime=datetime.now()
        )

        # Add the new configuration to the session
        self.session.add(new_config)
        self.session.commit()  # Commit the transaction

    def delete_all_notification_configuration_by_user_id(self, user_id):
        try:
            # Use parameterized query to avoid SQL injection
            delete_query = text("DELETE FROM [estdco].[CODAL].[notification_configurations] WHERE user_id = :user_id")
            self.session.execute(delete_query, {'user_id': user_id})
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"An error occurred: {e}")

    def delete_notification_configuration(self, config: NotificationConfiguration):
        try:
            # Check if the given configuration exists in the session
            existing_config = self.session.query(NotificationConfiguration).filter_by(
                user_id=config.user_id,
                including=config.including,
                excluding=config.excluding,
                publisher_national_code=config.publisher_national_code,
                letter_types=config.letter_types,
                period=config.period,
                lettersChecked=config.lettersChecked,
                attachmentsChecked=config.attachmentsChecked,
                created_datetime=config.created_datetime
            ).first()

            if existing_config:
                self.session.delete(existing_config)
                self.session.commit()
                print("Configuration deleted successfully")
            else:
                print("Configuration does not exist and cannot be deleted")

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"An error occurred: {e}")

    def get_all_groups(self):
        query_result = self.session.query(LetterType).from_statement(
            text(
                "SELECT * FROM [estdco].[CODAL].[letter_types];")
        ).all()

        return query_result

    def get_all_symbols(self):
        # Query the view and return the results
        query_result = self.session.query(Publisher).from_statement(
            text("""
            SELECT TOP (1000) 
                [persian_symbol_name] AS [Symbol],
                [National Code] AS [National_Code]
            FROM [estdco].[web].[publisher_info_filtered]
            WHERE (Status = N'پذيرفته شده در بورس تهران' OR Status = N'پذيرفته شده در فرابورس ايران')
              AND english_company_name NOT LIKE '%Fund%'
              AND english_company_name NOT LIKE '%fund%'
              AND english_symbol_name NOT LIKE '%Fund%'
              AND english_symbol_name NOT LIKE '%fund%'
            """)
        ).all()

        return query_result

    def get_all_letters(self):

        letters = self.session.query(Letter).from_statement(
            text(
                "SELECT TOP (100) *, [National Code] AS National_Code FROM estdco.CODAL.combined_dropdown_data ORDER BY PublishDateTime DESC;")
        ).all()

        return [Letter.to_dict(letter) for letter in letters]

    def get_relative_data(self, source_type=None, from_date=None, to_date=None, main_group=None, category_group=None,
                          sub_category_group=None,
                          producer_group=None):
        print(f"source value: {source_type}")
        print(f"type: {type(source_type)}")
        source_type = str(source_type)
        main_group = None
        producer_group = None
        from_date = "1402/06/23"
        to_date = "1403/06/01"

        query_type = self.session.query(Sources).from_statement(
            text("SELECT * FROM ime.sources WHERE code = :code")
        ).params(code=source_type).first()

        table_name = query_type.TableNameMap
        query_data = None

        if source_type == "1":
            start_time = time.time()  # Record the start time

            query_data = self.session.query(CommodityExchangeArzeh).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_arzeh(:from_date, :to_date, :producerId, :mainGroupId)")
            ).params(from_date=from_date, to_date=to_date, producerId=producer_group, mainGroupId=main_group).all()

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f"{len(query_data)} of rows found")
            print(f"Query execution time: {elapsed_time} seconds")

        elif source_type == "2":
            start_time = time.time()  # Record the start time

            query_data = self.session.query(CommodityExchangePhysical).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_physical(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f"{len(query_data)} of rows found")
            print(f"Query execution time: {elapsed_time} seconds")

        elif source_type == "3":
            start_time = time.time()  # Record the start time

            query_data = self.session.query(CommodityExchangeExport).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_export(:from_date, :to_date, :producerId, :mainGroupId)")
            ).params(from_date=from_date, to_date=to_date, producerId=producer_group, mainGroupId=main_group).all()

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f"{len(query_data)} of rows found")
            print(f"Query execution time: {elapsed_time} seconds")

        return query_data, table_name

    def get_notitification_configutaion_by_user_id(self, user_id):

        query_result = self.session.query(NotificationConfiguration).from_statement(
            text(
                f"SELECT * FROM [estdco].[CODAL].[notification_configurations] Where user_id = '{user_id}';")
        ).all()

        notif_dict = None
        if query_result:
            notif_dict = NotificationConfiguration().combine_notification_configs(query_result)
        return notif_dict

    def get_notitification_configutaion_by_user_id_list(self, user_id):
        query_result = self.session.query(NotificationConfiguration).from_statement(
            text(
                f"SELECT DISTINCT * FROM [estdco].[CODAL].[notification_configurations] WHERE user_id = '{user_id}';"
            )
        ).all()

        return query_result

    def get_notification_content(self, username):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CommodityExchangeExport).from_statement(
            text(
                f"SELECT * FROM CODAL.filtered_letters_for_notifications(:username)")
        ).params(username=username).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

    # User Notifications CRUD Operations
    # Create a user notification by user_id and tracingNo
    def create_user_notification(self, user_id, tracingNo):
        new_notification = UserNotification(user_id=user_id, tracingNo=tracingNo)
        self.session.add(new_notification)
        self.session.commit()
        return new_notification

    # Read a user notification by user_id and tracingNo
    def read_user_notification(self, user_id, tracingNo):
        try:
            notification = self.session.query(UserNotification).filter_by(user_id=user_id, tracingNo=tracingNo).one()
            return notification
        except NoResultFound:
            return None

    # Update a user notification
    def update_user_notification(self, user_id, tracingNo, new_user_id=None, new_tracingNo=None):
        notification = self.read_user_notification(user_id, tracingNo)
        if notification:
            if new_user_id:
                notification.user_id = new_user_id
            if new_tracingNo:
                notification.tracingNo = new_tracingNo
            self.session.commit()
            return notification
        else:
            return None

    # Delete a user notification
    def delete_user_notification(self, user_id, tracingNo):
        notification = self.read_user_notification(user_id, tracingNo)
        if notification:
            self.session.delete(notification)
            self.session.commit()
            return True
        else:
            return False

    def process_notitification_configutaion_by_username(self, user_id):
        try:
            # Execute the stored procedure using SQLAlchemy
            stmt = text("EXEC [CODAL].[ProcessNotificationConfiguration] @userId = :user_id")
            self.session.execute(stmt, {"user_id": user_id})
            self.session.commit()
            return True
        except Exception as e:
            # Handle exceptions, such as database errors
            print(f"An error occurred: {str(e)}")
            self.session.rollback()
            return False

    def get_notification_n_not_seen(self, user_id):
        start_time = time.time()  # Record the start time

        # Execute the query to fetch notifications for the specified user_id
        notifications = self.session.query(UserNotification).filter_by(user_id=user_id).count()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time

        return notifications

    def get_letters_notifs_by_user_id(self, user_id):
        query_data = self.session.query(Letter).from_statement(
            text(
                "SELECT * FROM [CODAL].[filtered_letters_for_notifications](:user_id)"
            )
        ).params(user_id=user_id).all()

        keywords = self.get_notification_config_keywords_by_user(user_id)

        # Create a dictionary to store the grouped results
        grouped_data = defaultdict(lambda: {
            'TracingNo': None,
            'Symbol': None,
            'Title': None,
            'PublishDateTime': None,
            'persian_company_name': None,
            'Url': None,
            'AttachmentUrl': None,
            'Isseen': None,
            'containingWords': {keyword: 0 for keyword in keywords}  # Initialize all keywords with count 0
        })

        for item in query_data:
            letter_dict = item.to_dict()
            tracing_no = letter_dict['TracingNo']

            # Initialize the group if it is the first occurrence
            if grouped_data[tracing_no]['TracingNo'] is None:
                grouped_data[tracing_no].update({
                    'TracingNo': letter_dict['TracingNo'],
                    'Symbol': letter_dict['Symbol'],
                    'Title': letter_dict['Title'],
                    'PublishDateTime': letter_dict['PublishDateTime'],
                    'persian_company_name': letter_dict['persian_company_name'],
                    'Url': letter_dict['Url'],
                    'AttachmentUrl': letter_dict['AttachmentUrl'],
                    'Isseen': letter_dict['Isseen']
                })

            # Aggregate the containingWords
            for keyword, count in letter_dict['containingWords'].items():
                grouped_data[tracing_no]['containingWords'][keyword] += int(count)

        # Convert the grouped_data to a list of dictionaries
        result_data = list(grouped_data.values())

        return result_data

    def delete_all_notifications_by_user_id(self, user_id):
        try:
            # Use parameterized query to avoid SQL injection
            delete_query = text("DELETE FROM [estdco].[web].[Users_Notification] WHERE user_id = :user_id")
            self.session.execute(delete_query, {'user_id': user_id})
            self.session.commit()
            print(f"Deleted all notifications for user_id {user_id}")

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"An error occurred: {e}")

    def get_notification_config_keywords_by_user(self, user_id):
        try:
            # Use parameterized query to avoid SQL injection
            query = text(
                "SELECT DISTINCT TOP (1000) [including] FROM [estdco].[CODAL].[notification_configurations] WHERE user_id = :user_id"
            )
            result = self.session.execute(query, {'user_id': user_id})
            keywords = [row[0] for row in result.fetchall()]

            return keywords

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"An error occurred: {e}")
            return []
