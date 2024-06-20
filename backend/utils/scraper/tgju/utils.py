def extract_number_from_span(span_html):
    """
        Extract the numeric value from a span HTML element.

        Parameters:
        - span_html (str): HTML string containing a span element.

        Returns:
        - float: Extracted numeric value with the appropriate sign.
        """
    if span_html:
        try:
            value_str = span_html.split('">')[-1].split('<')[0].replace(',', '')
            value = str(float(value_str[:-1]) / 100 if value_str.endswith('%') else float(value_str))

            if 'high' in span_html:
                return value
            elif 'low' in span_html:
                return "-" + value
            else:
                return None
        except (ValueError, IndexError, TypeError):
            return None


def find_tables_with_name(soup, tables_name):
    tgju_widgets = soup.find_all('div', class_='tgju-widget')

    for widget in tgju_widgets:

        if tables_name == "عملکرد":
            title_div = widget.find('div', class_='tgju-widget-title')
            title = title_div.find('h2') if title_div else None
            if title:
                table = widget.find('table', class_='table')
                if table and tables_name in title.text.strip():
                    return table

        else:
            title = widget.find('h2')

            if title:
                table = widget.find('table', class_='table')
                if table and tables_name in title.text.strip():
                    return table
