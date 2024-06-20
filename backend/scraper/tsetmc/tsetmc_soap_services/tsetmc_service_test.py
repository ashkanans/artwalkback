from datetime import datetime, timedelta

from backend.scraper.tsetmc.service.tse_client_instrument_and_share_service import TseClientInstrumentAndShareService
from backend.scraper.tsetmc.tsetmc_soap_services.tsetmc_service_base import *

# Get instrument and share from web service
instrument_and_share = get_instrument_and_share(0, 0)


# process instrument_and_share and generate instrument info list
tse_client_instrument_info = generateInstrument(instrument_and_share)

# process instrument_and_share and generate share info list
tse_client_share_info = generateShare(instrument_and_share)

# Create a datetime object to retrieve data from the past 10 years.
current_datetime = datetime.now()
new_datetime = current_datetime - timedelta(days=3650)
for item in tse_client_instrument_info:
    closingPrice = getInsturmentClosingPrice(item.insCode)

    new_closing_price_list = calculateAdjustedPrice(2,new_datetime,item.insCode,closingPrice,tse_client_share_info,tse_client_instrument_info)


tse_instrument_and_share_service = TseClientInstrumentAndShareService()
tse_instrument_and_share_service.create_table_share_info()
# res_instrument = tse_instrument_and_share_service.add_or_update_instrument_info(tse_client_instrument_info)
res_share = tse_instrument_and_share_service.add_or_update_share_info(tse_client_share_info)