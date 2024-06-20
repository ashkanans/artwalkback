from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tradingeconomics.service.profiles_history_service import ProfilesHistoryService


# https://markets.tradingeconomics.com/chart/co1:com?span=1m&securify=new&url=/commodity/brent-crude-oil&AUTH=wJvneR%2BjXl7E2XK8TZwGU5govGBp1rV2mGRA3NnRZBwgJ8vrPb%2FM60zjkV6r7V8H&ohlc=0
# TODO mr.Rastegar check this data
#  I found a url address so we could get history of all symbol like Brent
#  this address used by summary chart in this address
#  https://tradingeconomics.com/commodity/brent-crude-oil
#  This is the json structure
#  {
#   "d1": "2023-12-16T18:40:38.7925735+00:00",
#   "d2": "2024-01-15T18:40:38.7925735+00:00",
#   "agr": "1h",
#   "series": [
#     {
#       "symbol": "CO1:COM",
#       "name": "Brent",
#       "shortname": "Brent",
#       "full_name": "Brent Crude Oil",
#       "data": [
#         {
#           "open": 77.2873,
#           "high": 77.4064,
#           "low": 77.068,
#           "close": 77.103,
#           "date": "2023-12-18T00:01:00",
#           "x": 1702857660000,
#           "y": 77.103,
#           "percentChange": null,
#           "change": null
#         },
#         {
#           "open": 77.0932,
#           "high": 77.1974,
#           "low": 76.848,
#           "close": 77.0209,
#           "date": "2023-12-18T01:00:00",
#           "x": 1702861200000,
#           "y": 77.0209,
#           "percentChange": -0.106,
#           "change": -0.0821
#         },
#         {
#           "open": 77.0336,
#           "high": 77.1678,
#           "low": 77.0016,
#           "close": 77.0051,
#           "date": "2023-12-18T02:00:00",
#           "x": 1702864800000,
#           "y": 77.0051,
#           "percentChange": -0.021,
#           "change": -0.0158
#         }
#       ],
#       "forecast": null,
#       "unit": "USD/Bbl",
#       "decimals": 3,
#       "frequency": "intraday",
#       "type": "commodity",
#       "allowed_candles": true
#     }
#   ],
#   "allow_intraday": true,
#   "allow_interval": "1m",
#   "isIntraday": true,
#   "chartFrequency": "intraday",
#   "span": "1m"
#  }
class ProfilesHistoryScraper(BaseScraper):
    def process_data(self, json_data):
        profiles_history_data = json_data.get("series", [])

        if profiles_history_data:

            profiles_history_service = ProfilesHistoryService()

            profiles_history_service.create_table()
            self.logger.info(f"profiles_history table Created")

            profiles_history_list = []
            for element in profiles_history_data:
                annId = element.get("name")
                for dataItem in element.get("data"):
                    price = dataItem.get("y")
                    date = dataItem.get("date")
                    profiles_history_list.append(
                        {
                            'AnnID': annId,
                            'price': price,
                            'date': date,
                            'open': dataItem.get("open"),
                            'high': dataItem.get("high"),
                            'low': dataItem.get("low"),
                            'close': dataItem.get("close"),
                            'percentChange': dataItem.get("percentChange"),
                            'change': dataItem.get("change")
                        }
                    )

            profiles_history_service.update_profiles_history(profiles_history_list)

            self.logger.info("profiles history retrieved successfully.")
        else:
            self.logger.warning("profiles history could not be retrieved.")
