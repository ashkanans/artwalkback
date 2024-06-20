from collections import defaultdict

from sqlalchemy import Column, Integer, BigInteger, Sequence, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LettersColumnHeadersMap(Base):
    __tablename__ = 'codal_letters_column_headers_map'

    id = Column(Integer, primary_key=True)
    insCode = Column(BigInteger)
    symbol = Column(Unicode(50))
    header_key = Column(Unicode(50))
    header_value = Column(Unicode(50))


class LettersRowHeaders(Base):
    __tablename__ = 'codal_letters_row_headers'

    id = Column(Unicode(50), Sequence('Seq_codal_letters_row_headers'), primary_key=True)
    insCode = Column(BigInteger)
    symbol = Column(Unicode(50))
    header_key = Column(Unicode(50))
    header_item = Column(Unicode(50))


def convert_to_format(rows):
    """Converts a list of LettersRowHeaders to the desired format.

    Args:
        rows (list): A list of LettersRowHeaders objects.

    Returns:
        dict: A dictionary in the desired format.
    """
    # Create a defaultdict to store the data
    result = defaultdict(list)
    column_headers_map = [
        "تعداد تولید",
        "تعداد فروش",
        "مبلغ فروش (میلیون ریال)",
        "نرخ فروش (ریال)",
    ]
    # Iterate over each LettersRowHeaders object
    for row in rows:
        # Append the header_item to the list corresponding to its header_key
        result[row.header_key].append(row.header_item)

    result = dict(result)
    final_results = {}
    for key, values in result.items():
        formatted_results = {}
        for header in column_headers_map:
            formatted_results[header] = values
        final_results[key] = formatted_results

    return final_results
