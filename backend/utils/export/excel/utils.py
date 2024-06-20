import re
from datetime import datetime

from khayyam import JalaliDatetime

from backend.scraper.cbi.service.inflation_rate_yearly_service import InflationRateYearlyService
from backend.scraper.codal.model.cells import Cells
from backend.scraper.fipiran.service.index_service import IndexService
from backend.scraper.ime.model.physical_transaction import PhysicalTransaction
from backend.scraper.ime.service.physical_transaction_service import PhysicalTransactionService
from backend.scraper.tgju.service.profiles_at_a_glance_service import ProfilesAtAGlanceService
from backend.scraper.tgju.service.profiles_service import ProfilesService
from backend.scraper.tgju.service.profiles_summary_service import ProfilesSummaryService


def excel_cell_to_row_col(cell_address):
    match = re.match(r'([A-Z]+)(\d+)', cell_address)
    if match:
        col_str, row_str = match.groups()
        return col_str, int(row_str)
    else:
        raise ValueError("Invalid Excel cell address format")


def calculate_proper_address(col, row, final_filled, based_on):
    if based_on == "row":
        if int(row) >= final_filled:
            return f"{col}{int(row)}"
        else:
            return f"{col}{int(row) + final_filled + 2}"
    else:
        char_int = column_char_to_int(col)
        if char_int > final_filled:
            return f"{col}{int(row)}"
        else:
            char_int = column_char_to_int(col)
            new_col = char_int + final_filled - 1
            return f"{column_int_to_char(new_col)}{row}"


def column_char_to_int(char):
    char = char.upper()
    result = 0

    for i, c in enumerate(reversed(char)):
        result += (ord(c) - ord('A') + 1) * (26 ** i)

    return result


def column_int_to_char(num):
    if num <= 0:
        return None

    result = ""
    while num:
        remainder = (num - 1) % 26
        result = chr(remainder + ord('A')) + result
        num = (num - 1) // 26

    return result


def decreament_address_by_value(address, param, value):
    for i in range(value):
        address = decreament_address(address, param)
    return address


def filtered_cells_by_monthly_performance(cells_list):
    target_value = "دوره یک ماهه منتهی به"
    target_cell = next((cell for cell in cells_list if target_value in cell.value), None)
    target_col, target_row = excel_cell_to_row_col(target_cell.address)

    if target_cell:
        # Extract the first letter of the address
        first_letter = target_cell.address[0]

        # Calculate the new columns
        new_columns = [chr(ord(first_letter) + i + 1) for i in range(3)]

        # Calculate the distance between the target cell address character and 'B'
        distance = ord(first_letter) - ord('B')

        filtered_cells_final = []
        # Move the cells from N to Q to B to E
        for cell in cells_list:
            if first_letter <= cell.address[0] <= new_columns[-1]:
                new_address = chr(ord(cell.address[0]) - distance) + cell.address[1:]
                if target_row > 1:
                    new_address = decreament_address_by_value(new_address, "row-wise", target_row)
                cell.address = new_address
                filtered_cells_final.append(cell)
            elif 'A' in cell.address[0]:
                new_address = cell.address
                if target_row > 1:
                    new_address = decreament_address_by_value(new_address, "row-wise", target_row)
                cell.address = new_address
                filtered_cells_final.append(cell)

        return filtered_cells_final
    else:
        print("Target cell not found.")
        return None


def increament_address(cell_address, param):
    column, row = excel_cell_to_row_col(cell_address)
    if param == "column-wise":
        col_int = column_char_to_int(column)
        col_int += 1
        col_new = column_int_to_char(col_int)
        return f"{col_new}{row}"
    else:
        return f"{column}{row + 1}"


def decreament_address(cell_address, param):
    column, row = excel_cell_to_row_col(cell_address)
    if param == "column-wise":
        col_int = column_char_to_int(column)
        col_int -= 1
        col_new = column_int_to_char(col_int)
        return f"{col_new}{row}"
    else:
        return f"{column}{row - 1}"


def find_value_B(cells, value_A, param, header_key, header_cells_address):
    for cell in cells:
        column, row = excel_cell_to_row_col(cell.address)
        column_header = f"{column}2"
        row_header = f"A{row}"

        column_header_cell = next((cell for cell in cells if cell.address == column_header), None)
        row_header_cell = next((cell for cell in cells if cell.address == row_header), None)

        if (column_header_cell.value and row_header_cell.value and row_header_cell.value.strip() == value_A.strip()
                and column_header_cell.value.strip() == param.strip()):
            if 'فروش داخلی' == header_key and header_cells_address[0][0] < row < header_cells_address[1][0]:
                return cell.value
            elif 'فروش صادراتی' == header_key and header_cells_address[1][0] < row < header_cells_address[2][0]:
                return cell.value
            elif 'درآمد ارائه خدمات' == header_key and header_cells_address[2][0] < row < header_cells_address[3][0]:
                return cell.value
            elif 'برگشت از فروش' == header_key:
                return cell.value


def make_cells_custumized_based_on_headers(filtered_cells, headers_dict, header_cells):
    header_cells_address = []
    for cells in header_cells:
        col, row = excel_cell_to_row_col(cells.address)
        header_cells_address.append([row, col])

    custumized_cells = []

    cell_address_B = "B1"
    cell_address_A = "A4"

    target_cell = next((cell for cell in filtered_cells if cell.address == cell_address_B), None)
    target_cell.value = convert_to_persian_month(target_cell.value)
    custumized_cells.append(Cells(address=cell_address_B, value=target_cell.value))

    for header_key, header_items in headers_dict.items():
        custumized_cells.append(Cells(address=cell_address_A, value=header_key))
        cell_address_A = increament_address(cell_address_A, "row-wise")

        for key, values in header_items.items():
            custumized_cells.append(Cells(address=cell_address_A, value=key))

            for value_A in values:
                cell_address_A = increament_address(cell_address_A, "row-wise")
                cell_address_B = increament_address(cell_address_A, "column-wise")

                value_B = find_value_B(filtered_cells, value_A, key, header_key, header_cells_address)
                custumized_cells.append(Cells(address=cell_address_A, value=value_A))
                custumized_cells.append(Cells(address=cell_address_B, value=value_B))

            cell_address_A = increament_address(cell_address_A, "row-wise")
            custumized_cells.append(Cells(address=cell_address_A, value=""))
            cell_address_A = increament_address(cell_address_A, "row-wise")

    return custumized_cells


def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key


def make_sector_cells_custumized_based_on_headers(indexes, listOfClosingPrice, sector_prices_headers, fipiran_index,
                                                  second_table_headers):
    cells = []

    indexes_address = "A1"
    for index in indexes:
        cells.append(Cells(address=indexes_address, value=index))
        second_table_headers.append(index)
        for i in range(len(sector_prices_headers)):
            indexes_address = increament_address(indexes_address, "column-wise")

    indexes_address = increament_address(indexes_address, "column-wise")
    second_tables_address = indexes_address
    for header in second_table_headers:
        cells.append(Cells(address=second_tables_address, value=header))
        second_tables_address = increament_address(second_tables_address, "column-wise")

    header_address = "A2"
    for index in indexes:
        for key, value in sector_prices_headers.items():
            cells.append(Cells(address=header_address, value=value))
            header_address = increament_address(header_address, "column-wise")
    indexServices = IndexService()

    base_address_org = "A3"
    base_address = "A3"
    table_second = []
    for list in listOfClosingPrice:
        element_address = base_address_org
        table_second_dict = {}
        for element in list:
            formatted_date_gregorian = datetime.strptime(element.datetime_str, "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d")

            # Convert Gregorian date to Solar date
            gregorian_date = datetime.strptime(formatted_date_gregorian, "%Y-%m-%d")
            solar_date = JalaliDatetime(gregorian_date)

            # Add the Solar date to the Cells object
            cells.append(Cells(address=element_address, value=solar_date.strftime("%Y-%m-%d")))

            element_address = increament_address(element_address, "column-wise")
            cells.append(Cells(address=element_address, value=float(element.priceFirst)))

            element_address = increament_address(element_address, "column-wise")
            cells.append(Cells(address=element_address, value=float(element.pDrCotVal)))

            element_address = increament_address(element_address, "column-wise")
            cells.append(Cells(address=element_address, value=float(element.priceMin)))

            element_address = increament_address(element_address, "column-wise")
            cells.append(Cells(address=element_address, value=float(element.priceMax)))

            element_address = increament_address(element_address, "column-wise")

            cells.append(Cells(address=element_address, value=float(element.qTotTran5J)))
            table_second_dict[solar_date.strftime("%Y-%m-%d")] = element.pDrCotVal

            base_address = increament_address(base_address, "")
            element_address = base_address
        table_second.append(table_second_dict)
        for i in range(len(sector_prices_headers)):
            base_address_org = increament_address(base_address_org, "column-wise")
            base_address = base_address_org

    original_second_table_address = increament_address(base_address, "column-wise")
    longest_dict = max(table_second, key=lambda d: len(d))
    for key, value in longest_dict.items():
        second_table_address = original_second_table_address

        cells.append(Cells(address=second_table_address, value=key))
        second_table_address = increament_address(second_table_address, "column-wise")

        for index_org, index_values in fipiran_index.items():
            found_index = next((index for index in index_values if
                                getattr(index, 'solar_date',
                                        None) == key),
                               None)
            if found_index:
                cells.append(Cells(address=second_table_address, value=found_index.value))
            else:
                cells.append(Cells(address=second_table_address, value=""))
            second_table_address = increament_address(second_table_address, "column-wise")

        for table in table_second:
            try:
                price = table[key]
                cells.append(Cells(address=second_table_address, value=price))
            except Exception as e:
                cells.append(Cells(address=second_table_address, value=""))
            second_table_address = increament_address(second_table_address, "column-wise")

        original_second_table_address = increament_address(original_second_table_address, "")
    return cells


def make_IRRTD_custumized_based_on_headers(indexes, headers):
    cells = []

    headers_address = "A1"
    for header in headers:
        cells.append(Cells(address=headers_address, value=header))
        headers_address = increament_address(headers_address, "column-wise")

    indexes_address_base = "A2"
    for index in indexes:
        indexes_address = indexes_address_base
        cells.append(Cells(address=indexes_address, value=index.get("name")))
        indexes_address = increament_address(indexes_address, "column-wise")
        cells.append(Cells(address=indexes_address, value=index.get("unit")))
        indexes_address = increament_address(indexes_address, "column-wise")

        if index.get("name") == "دلار":
            profilesAtAGlanceService = ProfilesAtAGlanceService()
            profiles = ProfilesService()
            profilesSummaryService = ProfilesSummaryService()

            profile = profiles.get_tgju_profile_by_nameFa("دلار")
            current = profilesAtAGlanceService.get_profile_at_a_glance_by_id(profile.Id)

            price1400 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1400")
            price1401 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1401")
            price1402 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1402")
            prices = [price1400, price1401, price1402, current.CurrentRate]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "دلار (نیما/خرید)":
            profilesAtAGlanceService = ProfilesAtAGlanceService()
            profiles = ProfilesService()
            profilesSummaryService = ProfilesSummaryService()

            profile = profiles.get_tgju_profile_by_nameFa("دلار (نیما/خرید)")
            current = profilesAtAGlanceService.get_profile_at_a_glance_by_id(profile.Id)

            price1400 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1400")
            price1401 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1401")
            price1402 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol, "1402")
            prices = [price1400, price1401, price1402, current.CurrentRate]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "بیلت صادراتی ایران":
            # Your code for handling "بیلت صادراتی ایران"
            pass
        elif index.get("name") == "بیلت فخوز":
            # Your code for handling "بیلت فخوز"
            pass
        elif index.get("name") == "لوب کات سنگین":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("لوب کات سنگین", "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("لوب کات سنگین", "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("لوب کات سنگین", "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("لوب کات سنگین")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.Price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "روغن پایه SN600":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("روغن پایه SN600",
                                                                                               "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("روغن پایه SN600",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("روغن پایه SN600",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("روغن پایه SN600")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.Price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "تورم":
            inflationRateYearlyService = InflationRateYearlyService()
            inf1400 = inflationRateYearlyService.get_inflation_rate_yearly_by_year("1400")
            inf1401 = inflationRateYearlyService.get_inflation_rate_yearly_by_year("1401")

            inflationRates = [inf1400.InflationRate, inf1401.InflationRate]

            for rate in inflationRates:
                cells.append(Cells(address=indexes_address, value=rate))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "برق":
            # Your code for handling "برق"
            pass
        elif index.get("name") == "گاز":
            # Your code for handling "گاز"
            pass
        elif index.get("name") == "حقوق دولتی سنگ آهنی ها":
            # Your code for handling "حقوق دولتی سنگ آهنی ها"
            pass
        elif index.get("name") == "نفتا":
            pass
            # commoditiesHistoryService = CommoditiesHistoryService()
            # price1400 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Naphtha","2021")
            # price1401 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Naphtha ", "2022")
            # price1402 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Naphtha", "2023")
            # lastPrice = commoditiesHistoryService.get_last_price_by_AnnId("Naphtha")
            #
            # prices = [price1400, price1401, price1402, lastPrice]
            #
            # for price in prices:
            #     cells.append(Cells(address=indexes_address, value=price))
            #     indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "نفت برنت":
            commoditiesHistoryService = CommoditiesHistoryService()
            price1400 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Brent", "2021")
            price1401 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Brent", "2022")
            price1402 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Brent", "2023")
            lastPrice = commoditiesHistoryService.get_last_price_by_AnnId("Brent")

            prices = [price1400, price1401, price1402, lastPrice]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "سنگ آهن دانه بندی":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("سنگ آهن دانه بندی",
                                                                                               "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("سنگ آهن دانه بندی",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("سنگ آهن دانه بندی",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("سنگ آهن دانه بندی")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.ArzeBasePrice))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "کنسانتره سنگ آهن":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("کنسانتره سنگ آهن",
                                                                                               "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("کنسانتره سنگ آهن",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("کنسانتره سنگ آهن",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("کنسانتره سنگ آهن")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.ArzeBasePrice))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "گندله سنگ آهن":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("گندله سنگ آهن",
                                                                                               "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("گندله سنگ آهن",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("گندله سنگ آهن",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("گندله سنگ آهن")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.ArzeBasePrice))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "آهن اسفنجی":
            physicalTransactionService = PhysicalTransactionService()
            # trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("آهن اسفنجی",
            #                                                                                    "1400")
            trans1400 = PhysicalTransaction(Price="")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("آهن اسفنجی",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("آهن اسفنجی",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("آهن اسفنجی")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.Price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "مس مفتول":
            physicalTransactionService = PhysicalTransactionService()
            trans1400 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("مس مفتول",
                                                                                               "1400")
            trans1401 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("مس مفتول",
                                                                                               "1401")
            trans1402 = physicalTransactionService.get_first_transaction_by_GoodsName_and_year("مس مفتول",
                                                                                               "1402")
            transLast = physicalTransactionService.get_last_transaction_by_GoodsName_and_year("مس مفتول")

            transactions = [trans1400, trans1401, trans1402, transLast]

            for element in transactions:
                cells.append(Cells(address=indexes_address, value=element.ArzeBasePrice))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "آلومینیوم":
            commoditiesHistoryService = CommoditiesHistoryService()
            price1400 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Aluminum", "2021")
            price1401 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Aluminum", "2022")
            price1402 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Aluminum", "2023")
            lastPrice = commoditiesHistoryService.get_last_price_by_AnnId("Aluminum")

            prices = [price1400, price1401, price1402, lastPrice]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "دلار/یورو":
            commoditiesHistoryService = CommoditiesHistoryService()
            price1400 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("EURUSD", "2021")
            price1401 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("EURUSD", "2022")
            price1402 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("EURUSD", "2023")
            lastPrice = commoditiesHistoryService.get_last_price_by_AnnId("EURUSD")

            prices = [price1400, price1401, price1402, lastPrice]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        elif index.get("name") == "مس":
            commoditiesHistoryService = CommoditiesHistoryService()
            price1400 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Copper", "2021")
            price1401 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Copper", "2022")
            price1402 = commoditiesHistoryService.get_first_price_by_AnnId_and_year("Copper", "2023")
            lastPrice = commoditiesHistoryService.get_last_price_by_AnnId("Copper")

            prices = [price1400, price1401, price1402, lastPrice]

            for price in prices:
                cells.append(Cells(address=indexes_address, value=price))
                indexes_address = increament_address(indexes_address, "column-wise")

        else:
            # Default case if none of the conditions match
            pass

        indexes_address_base = increament_address(indexes_address_base, "")

    return cells


def convert_to_persian_month(input_date_str):
    input_date_str = input_date_str.replace("دوره یک ماهه منتهی به ", "")
    input_date_str = input_date_str[:-2] + '25'
    # Split the date string into year, month, and day components
    year, month, day = map(int, input_date_str.split('/'))
    # Adjust the day if it's 31 to 30
    if day == 31:
        day = 30
    # Convert the input date components to a datetime object
    input_date = datetime(year, month, day)
    # Define a list of Persian month names
    persian_month_names = [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر',
        'دی', 'بهمن', 'اسفند'
    ]
    # Create the Persian month name based on the month number
    persian_month_name = persian_month_names[month - 1]
    # Create the final Persian date string
    persian_date_str = f'{persian_month_name} {year}'
    return persian_date_str


def get_first_Column_of_table(table):
    result = []
    for cell in table:
        if 'A' in cell.address:
            if cell.value:
                if 'شرح' not in cell.value and 'اوليه' not in cell.value and 'جمع' not in cell.value:
                    result.append({cell.rowSequence: cell.value})

    return result


def get_header_by_row_code(code, headers):
    for value in headers:
        for key, value in value.items():
            if code == key:
                return value


def creat_customized_dict_product(cell_vale, cell_word_address):
    first_investment_section = ['C', 'D', 'E']
    product_section = ['F', 'G', 'H']
    adjustments_section = ['I', 'J', 'K']
    sale_section = ['L', 'M', 'N']
    end_investment_section = ['O', 'P', 'Q']

    dict = {}

    if cell_word_address in first_investment_section:
        if cell_word_address == 'C':
            dict['موجودي اول دوره'] = {'مقدار': cell_vale}
        elif cell_word_address == 'D':
            dict['موجودي اول دوره'] = {'نرخ - ریال': cell_vale}
        else:
            dict['موجودي اول دوره'] = {'بهای تمام شده - میلیون ریال': cell_vale}

    elif cell_word_address in product_section:
        if cell_word_address == 'F':
            dict['تولید'] = {'مقدار': cell_vale}
        elif cell_word_address == 'G':
            dict['تولید'] = {'نرخ - ریال': cell_vale}
        else:
            dict['تولید'] = {'بهای تمام شده - میلیون ریال': cell_vale}

    elif cell_word_address in adjustments_section:
        if cell_word_address == 'I':
            dict['تعدیلات'] = {'مقدار': cell_vale}
        elif cell_word_address == 'J':
            dict['تعدیلات'] = {'نرخ - ریال': cell_vale}
        else:
            dict['تعدیلات'] = {'بهای تمام شده - میلیون ریال': cell_vale}

    elif cell_word_address in sale_section:
        if cell_word_address == 'L':
            dict['فروش'] = {'مقدار': cell_vale}
        elif cell_word_address == 'M':
            dict['فروش'] = {'نرخ - ریال': cell_vale}
        else:
            dict['فروش'] = {'بهای تمام شده - میلیون ریال': cell_vale}

    elif cell_word_address in end_investment_section:
        if cell_word_address == 'O':
            dict['موجودی پایان دوره'] = {'مقدار': cell_vale}
        elif cell_word_address == 'P':
            dict['موجودی پایان دوره'] = {'نرخ - ریال': cell_vale}
        else:
            dict['موجودی پایان دوره'] = {'بهای تمام شده - میلیون ریال': cell_vale}

    return dict

def creat_customized_dict_requirement(cell_vale, cell_word_address):
    first_investment_section = ['C', 'D', 'E']
    product_section = ['F', 'G', 'H']
    adjustments_section = ['I', 'J', 'K']
    end_investment_section = ['L', 'M', 'N']


    dict = {}

    if cell_word_address in first_investment_section:
        if cell_word_address == 'C':
            dict['موجودي اول دوره'] = {'مقدار': cell_vale}
        elif cell_word_address == 'D':
            dict['موجودي اول دوره'] = {'نرخ - ریال': cell_vale}
        else:
            dict['موجودي اول دوره'] = {'مبلغ - میلیون ریال': cell_vale}

    elif cell_word_address in product_section:
        if cell_word_address == 'F':
            dict['خريد طي دوره'] = {'مقدار': cell_vale}
        elif cell_word_address == 'G':
            dict['خريد طي دوره'] = {'نرخ - ریال': cell_vale}
        else:
            dict['خريد طي دوره'] = {'مبلغ - میلیون ریال': cell_vale}

    elif cell_word_address in adjustments_section:
        if cell_word_address == 'I':
            dict['مصرف'] = {'مقدار': cell_vale}
        elif cell_word_address == 'J':
            dict['مصرف'] = {'نرخ - ریال': cell_vale}
        else:
            dict['مصرف'] = {'مبلغ - میلیون ریال': cell_vale}


    elif cell_word_address in end_investment_section:
        if cell_word_address == 'L':
            dict['موجودی پایان دوره'] = {'مقدار': cell_vale}
        elif cell_word_address == 'M':
            dict['موجودی پایان دوره'] = {'نرخ - ریال': cell_vale}
        else:
            dict['موجودی پایان دوره'] = {'مبلغ - میلیون ریال': cell_vale}

    return dict


def fill_customized_dict(total_dic, product, small_dict):
    sub1 = list(small_dict.keys())[0]
    sub2 = list(small_dict.values())[0]
    sub3 = list(sub2.keys())[0]
    sub4 = list(sub2.values())[0]
    if product in total_dic:
        if sub1 in total_dic[product]:
            total_dic[product][sub1].update(sub2)
        else:
            total_dic[product].update(small_dict)
    else:
        total_dic[product] = small_dict

    return total_dic


def create_sheet_template_product(work_sheet, headers, last_row):
    for header in headers:
        work_sheet['A' + last_row] = header
        work_sheet['B' + last_row] = 'موجودي اول دوره'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'بهای تمام شده - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'تولید'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'بهای تمام شده - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'تعدیلات'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'بهای تمام شده - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'فروش'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'بهای تمام شده - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'موجودی پایان دوره'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'بهای تمام شده - میلیون ریال'
        last_row = str(int(last_row) + 3)

    return work_sheet, last_row

def create_sheet_template_requirement(work_sheet, headers, last_row):
    for header in headers:
        work_sheet['A' + last_row] = header
        work_sheet['B' + last_row] = 'موجودي اول دوره'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'مبلغ - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'خريد طي دوره'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'مبلغ - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'مصرف'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'مبلغ - میلیون ریال'
        last_row = str(int(last_row) + 3)

        work_sheet['B' + last_row] = 'موجودی پایان دوره'

        work_sheet['C' + last_row] = 'مقدار'
        work_sheet['C' + str(int(last_row) + 1)] = 'نرخ - ریال'
        work_sheet['C' + str(int(last_row) + 2)] = 'مبلغ - میلیون ریال'
        last_row = str(int(last_row) + 3)

    return work_sheet, last_row
def fill_sheet_by_customized_dict_product(work_sheet, total_dict, last_row, last_column):
    for cell in work_sheet['A']:
        if cell.value:
            if cell.value in total_dict:
                sub_dict = total_dict[cell.value]

                sub_dict1 = sub_dict['موجودي اول دوره']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['بهای تمام شده - میلیون ریال']
                last_row=str(int(last_row) + 3)
                sub_dict1 = sub_dict['تولید']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['بهای تمام شده - میلیون ریال']
                last_row=str(int(last_row) + 3)
                sub_dict1 = sub_dict['تعدیلات']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['بهای تمام شده - میلیون ریال']
                last_row=str(int(last_row) + 3)
                sub_dict1 = sub_dict['فروش']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['بهای تمام شده - میلیون ریال']
                last_row=str(int(last_row) + 3)
                sub_dict1 = sub_dict['موجودی پایان دوره']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['بهای تمام شده - میلیون ریال']
                last_row=str(int(last_row) + 3)

    return work_sheet, last_row

def fill_sheet_by_customized_dict_requirement(work_sheet, total_dict, last_row, last_column):
    for cell in work_sheet['A']:
        if cell.value:
            if cell.value in total_dict:
                sub_dict = total_dict[cell.value]

                sub_dict1 = sub_dict['موجودي اول دوره']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['مبلغ - میلیون ریال']
                last_row=str(int(last_row) + 3)

                sub_dict1 = sub_dict['خريد طي دوره']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['مبلغ - میلیون ریال']
                last_row=str(int(last_row) + 3)

                sub_dict1 = sub_dict['مصرف']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['مبلغ - میلیون ریال']
                last_row=str(int(last_row) + 3)

                sub_dict1 = sub_dict['موجودی پایان دوره']
                work_sheet[last_column + last_row] = sub_dict1['مقدار']
                work_sheet[last_column + str(int(last_row) + 1)] = sub_dict1['نرخ - ریال']
                work_sheet[last_column + str(int(last_row) + 2)] = sub_dict1['مبلغ - میلیون ریال']
                last_row=str(int(last_row) + 3)

    return work_sheet, last_row