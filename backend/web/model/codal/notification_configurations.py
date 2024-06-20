from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NotificationConfiguration(Base):
    __tablename__ = 'notification_configurations'
    __table_args__ = {'schema': 'CODAL'}

    user_id = Column(String(500), primary_key=True)
    including = Column(String, primary_key=True)
    excluding = Column(String, primary_key=True)
    publisher_national_code = Column(String, primary_key=True)
    letter_types = Column(String(10), primary_key=True)
    period = Column(String(10), primary_key=True)
    lettersChecked = Column(Boolean, primary_key=True)
    attachmentsChecked = Column(Boolean, primary_key=True)
    created_datetime = Column(DateTime, primary_key=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'including': self.including,
            'excluding': self.excluding,
            'publisher_national_code': self.publisher_national_code,
            'letter_types': self.letter_types,
            'period': self.period,
            'lettersChecked': self.lettersChecked,
            'attachmentsChecked': self.attachmentsChecked,
            'created_datetime': self.created_datetime
        }

    def combine_notification_configs(self, configs):
        if not configs:
            return {}

        combined_dict = {
            'user_id': configs[0].user_id,
            'including': set(),
            'excluding': set(),
            'publisher_national_code': set(),
            'letter_types': set(),
            'period': set(),
            'lettersChecked': False,
            'attachmentsChecked': False,
            'created_datetime': max(config.created_datetime for config in configs)
        }

        for config in configs:
            combined_dict['including'].add(config.including)
            combined_dict['excluding'].add(config.excluding)
            combined_dict['publisher_national_code'].add(config.publisher_national_code)
            combined_dict['letter_types'].add(config.letter_types)
            combined_dict['period'].add(config.period)
            combined_dict['lettersChecked'] = combined_dict['lettersChecked'] or config.lettersChecked
            combined_dict['attachmentsChecked'] = combined_dict['attachmentsChecked'] or config.attachmentsChecked

        # Convert sets to comma-separated strings
        combined_dict['including'] = '، '.join(combined_dict['including'])
        combined_dict['excluding'] = '، '.join(combined_dict['excluding'])
        combined_dict['publisher_national_code'] = ','.join(combined_dict['publisher_national_code'])
        combined_dict['letter_types'] = ','.join(combined_dict['letter_types'])
        combined_dict['period'] = ','.join(combined_dict['period'])

        return combined_dict