import gzip
import io
import struct
import base64
from decimal import Decimal

from unicodedata import decimal
from zeep import Client

from backend.scraper.tsetmc.model import instrument_info
from backend.scraper.tsetmc.model.closing_price_info import ClosingPriceInfo
from backend.scraper.tsetmc.model.closing_price_info_adjusted import ClosingPriceInfoAdjusted
from backend.scraper.tsetmc.model.instrument_info import InstrumentInfo
from backend.scraper.tsetmc.model.tse_client_instrument_info import TseClientInstrumentInfo
from backend.scraper.tsetmc.model.tse_client_share_info import TseClientShareInfo
from backend.scraper.tsetmc.model.tsetmc_stock import TsetmcStock

# tseClient url
url = 'http://service.tsetmc.com/WebService/TseClient.asmx?wsdl'

# Compress parameter for sending to tse client web service
def compress(text):
    # Convert text to bytes using UTF-8 encoding
    bytes_data = text.encode('utf-8')

    # Compress bytes data using gzip
    with io.BytesIO() as memory_stream:
        with gzip.GzipFile(fileobj=memory_stream, mode='wb') as gzip_stream:
            gzip_stream.write(bytes_data)
        memory_stream.seek(0)
        compressed_data = memory_stream.read()

    # Prepend the length of the original uncompressed data as a 4-byte integer
    length_bytes = struct.pack('I', len(bytes_data))

    # Concatenate length_bytes and compressed_data
    result = length_bytes + compressed_data

    # Encode the result in Base64
    base64_encoded = base64.b64encode(result).decode('utf-8')

    return base64_encoded

# Get last_possible_deven data from tse client web service
def last_possible_deven():
    client = Client(url)
    # Calling LastPossibleDeven
    dates = client.service.LastPossibleDeven()
    return dates

# Get instrument and share info from tse client web service
def get_instrument_and_share(lastdeven, lastid):
    client = Client(url)
    # Calling InstrumentAndShare
    dates = client.service.InstrumentAndShare(lastdeven, lastid)
    return dates

# Split received string from InstrumentAndShare and generate a list of TseClientInstrumentInfo
def generateInstrument(res):
    result = res.split('@')[0].split(';')
    instrument_info_list = []
    for item in result:
        row = item.split(',')
        instrument_info = TseClientInstrumentInfo()
        instrument_info.insCode = int(row[0])
        instrument_info.instrumentID = row[1]
        instrument_info.latinSymbol = row[2]
        instrument_info.latinName = row[3]
        instrument_info.companyCode = row[4]
        instrument_info.symbol = row[5]
        instrument_info.name = row[6]
        instrument_info.cIsin = row[7]
        instrument_info.dEven = int(row[8])
        instrument_info.flow = int(row[9])
        instrument_info.lSoc30 = row[10]
        instrument_info.cGdSVal = row[11]
        instrument_info.cGrValCot = row[12]
        instrument_info.YMarNSC = row[13]
        instrument_info.CComVal = row[14]
        instrument_info.CSecVal = row[15]
        instrument_info.cSoSecVal = row[16]
        instrument_info.yVal = row[17]
        instrument_info_list.append(instrument_info)

    return instrument_info_list


# Get instrument info from tse client web service
def instrument(lastdeven, lastid):
    client = Client(url)
    res = get_instrument_and_share(lastdeven, lastid)
    return generateInstrument(res)

# Split received string from InstrumentAndShare and generate a list of TseClientShareInfo
def generateShare(res):
    result = res.split('@')[1].split(';')
    share_info_list = []
    for item in result:
        row = item.split(',')
        share_info = TseClientShareInfo.from_row(row)
        share_info_list.append(share_info)

    return share_info_list


# Get share info from tse client web service
def share(lastdeven, lastid):
    client = Client(url)
    res = get_instrument_and_share(lastdeven, lastid)
    return generateShare


# Get data from tse client Instrument web service
def instrument0(lastPossibleDeven):
    global stocks
    client = Client(url)

    if lastPossibleDeven is not None:
        resdates = lastPossibleDeven.split(';')
        # Calling Instrument with Deven retrieved from LastPossibleDeven service
        instrumentresult = client.service.Instrument(resdates[0])
        if instrumentresult is not None:
            stocks_entries = instrumentresult.split(';')
            stocks = [TsetmcStock(entry) for entry in stocks_entries]
            return stocks

# Get GetInsturmentClosingPrice from tse client web service
def getInsturmentClosingPrice(selectedInsCode):
    client = Client(url)

    if selectedInsCode is not None:
        insCode = compress(f"{selectedInsCode},0,0")
        closingPriceRes = client.service.DecompressAndGetInsturmentClosingPrice(insCode)
        closingPriceItems = closingPriceRes.split(';')
        closing_price_info_list = []

        if closingPriceItems is not None:
            for items in closingPriceItems:
                item = items.split(',')
                closing_price_info = ClosingPriceInfo(
                    insCode=item[0],
                    dEven=item[1],
                    pClosing=Decimal(item[2]),  # 100.50,
                    pDrCotVal=Decimal(item[3]),  # 99.75,
                    zTotTran=item[4],  # 5000,
                    qTotTran5J=item[5],  # 10000,
                    qTotCap=item[6],  # 500000,
                    priceMin=Decimal(item[7]),  # 99.25,
                    priceMax=Decimal(item[8]),  # 101.00,
                    priceYesterday=Decimal(item[9]),  # 99.80,
                    priceFirst=Decimal(item[10]),  # 100.00
                )
                closing_price_info_list.append(closing_price_info)
        return closing_price_info_list


def calculateAdjustedPriceMode1(closing_price_info_list):
    """
محاسبه     افزایش سود و سرمایه
    Args:
        closing_price_info_list:

    Returns:

    """
    d = 1
    # price_changes = [(reversed_prices[i] - reversed_prices[i + 1]) / reversed_prices[i + 1] * 100 for i in
    #                  range(len(reversed_prices) - 1)]
    for i in range(len(closing_price_info_list) - 2, 0, -1):
        d = d * closing_price_info_list[i + 1].PriceYesterday / closing_price_info_list[i].PClosing
    return d


def calculateAdjustedPrice(aAdjustPricesCondition, dateTime, selectedInsCode, cp, tseShareInfoList, InstrumentList):
    """

    Args:
        aAdjustPricesCondition: 1-"افزایش سود و سرمایه
        aAdjustPricesCondition: 2-افزایش سرمایه

        cp (ClosingPrice information for selected insCode):
    """
    startDeven = 0

    startDeven = int(dateTime.year * 10000 + dateTime.month * 100 + dateTime.day)
    num = 0

    cp = [p for p in cp if int(p.dEven) >= startDeven]
    if (aAdjustPricesCondition == 1 or aAdjustPricesCondition == 2) and len(cp) > 1:
        list_ = []

        d = 1
        list_.append(cp[-1])
        num2 = 0.0
        if aAdjustPricesCondition == 1:
            for k in range(len(cp) - 2, -1, -1):
                if cp[k].pClosing != cp[k + 1].priceYesterday:
                    num2 += 1
        if (aAdjustPricesCondition == 1 and num2 / len(cp) < 0.08) or aAdjustPricesCondition == 2:
            i = len(cp) - 2
            while i >= 0:
                if aAdjustPricesCondition == 1 and cp[i].pClosing != cp[i + 1].priceYesterday:
                    d = d * cp[i + 1].priceYesterday / cp[i].pClosing
                elif aAdjustPricesCondition == 2 and cp[i].pClosing != cp[i + 1].priceYesterday:
                    if any(p.insCode == selectedInsCode and p.dEven == cp[i + 1].dEven for p in tseShareInfoList):
                        share_old = next(
                            (p.numberOfShareOld for p in tseShareInfoList if p.insCode == selectedInsCode and p.dEven == cp[i + 1].DEven),
                            None)
                        share_new = next(
                            (p.numberOfShareNew for p in tseShareInfoList if p.insCode == selectedInsCode and p.dEven == cp[i + 1].DEven),
                            None)
                        if share_old is not None and share_new is not None and share_new != 0:
                            d *= share_old / share_new


                closing_price_info = ClosingPriceInfo(
                    insCode=cp[i].insCode,
                    dEven=cp[i].dEven,
                    pClosing=round(d * cp[i].pClosing, 2),
                    pDrCotVal=round(d * cp[i].pDrCotVal, 2),
                    zTotTran=cp[i].zTotTran,
                    qTotTran5J=cp[i].qTotTran5J,
                    qTotCap=cp[i].qTotCap,
                    priceMin=round(d * cp[i].priceMin),
                    priceMax=round(d * cp[i].priceMax),
                    priceYesterday=round(d * cp[i].priceYesterday),
                    priceFirst=round(d * cp[i].priceFirst, 2),
                )
                list_.append(closing_price_info)
                i -= 1

            closing_price_info_adjusted_list = []
            for cp in list_:
                closing_price_info_adjusted = (
                    ClosingPriceInfoAdjusted(cp.insCode, int(cp.dEven), float(cp.pClosing),
                                             float(cp.pDrCotVal), float(cp.priceMin), float(cp.priceMax),
                                             float(cp.priceYesterday), float(cp.priceFirst), aAdjustPricesCondition,
                                             float(cp.qTotCap), float(cp.qTotTran5J), float(cp.zTotTran)))
                closing_price_info_adjusted_list.append(closing_price_info_adjusted)
            return closing_price_info_adjusted_list

            #     list_.append({
            #         'insCode': cp[i].InsCode,
            #         'dEven': cp[i].dEven,
            #         'PClosing': round(d * cp[i].PClosing, 2),
            #         'PDrCotVal': round(d * cp[i].PDrCotVal, 2),
            #         'ZTotTran': cp[i].ZTotTran,
            #         'QTotTran5J': cp[i].QTotTran5J,
            #         'QTotCap': cp[i].QTotCap,
            #         'PriceMin': round(d * cp[i].PriceMin),
            #         'PriceMax': round(d * cp[i].PriceMax),
            #         'PriceYesterday': round(d * cp[i].PriceYesterday),
            #         'PriceFirst': round(d * cp[i].PriceFirst, 2)
            #     })
            #     i -= 1
            # cp.clear()
            # for j in range(len(list_) - 1, -1, -1):
            #     cp.append(list_[j])



def calculateAdjustedPrice0(closing_price_info_list, d):
    closing_prices = []

    for item in closing_price_info_list:
        closing_price_info = ClosingPriceInfo(
            ins_code=item.insCode,
            d_even=item.dEven,
            p_closing=round(d * item.PClosing, 2),
            p_dr_cot_val=round(d * item.PDrCotVal, 2),
            z_tot_tran=item.ZTotTran,
            q_tot_tran5j=item.QTotTran5J,
            q_tot_cap=item.QTotCap,
            price_min=round(d * item.PriceMin),
            price_max=round(d * item.PriceMax),
            price_yesterday=round(d * item.PriceYesterday, 2),
            price_first=round(d * item.PriceFirst, 2),
        )
        closing_prices.append(closing_price_info)
