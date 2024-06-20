from backend.scraper.cbi.service.inflation_rate_yearly_service import InflationRateYearlyService
from backend.scraper.ime.service.physical_transaction_service import PhysicalTransactionService
from backend.scraper.realtimedata.service.price_table_service import PriceTableService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_at_a_glance_service import ProfilesAtAGlanceService
from backend.scraper.tgju.service.profiles_service import ProfilesService
from backend.scraper.tgju.service.profiles_summary_service import ProfilesSummaryService
from backend.scraper.tradingeconomics.service.profiles_history_service import ProfilesHistoryService


class PriceTableScraper(BaseScraper):
    def process_data(self, data):

        price_table_service = PriceTableService()

        if not price_table_service.table_exists():
            price_table_service.create_table()
            self.logger.info("Created table: real_time_price_table")

        rows = []
        etp_column_maps = {
            "Naphtha": "نفتا",
            "Brent": "نفت برنت",
            "Aluminum": "آلومینیوم",
            "EURUSD": "دلار/یورو",
            "Copper": "نفتا"
        }
        currency_names_map = {
            "ime": ["لوب کات سنگین",
                    "روغن پایه SN600",
                    "سنگ آهن دانه بندی",
                    "کنسانتره سنگ آهن",
                    "گندله سنگ آهن",
                    "آهن اسفنجی",
                    "مس مفتول"
                    ],
            "tradingeconomics": ["Naphtha",
                                 "Brent",
                                 "Aluminum",
                                 "EURUSD",
                                 "Copper"
                                 ],
            "tgju": ["دلار",
                     "دلار (نیما/خرید)"],
            "cbi": ["تورم"],

        }

        for key, currencies in currency_names_map.items():
            for currency in currencies:
                row = {}
                if key == "tgju":
                    profilesAtAGlanceService = ProfilesAtAGlanceService()
                    profiles = ProfilesService()
                    profilesSummaryService = ProfilesSummaryService()

                    profile = profiles.get_tgju_profile_by_nameFa(currency)
                    priceCurrent = profilesAtAGlanceService.get_profile_at_a_glance_by_id(
                        profile.Id).CurrentRate.replace(",", "")

                    price1400 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol,
                                                                                         "1400").replace(",", "")
                    price1401 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol,
                                                                                         "1401").replace(",", "")
                    price1402 = profilesSummaryService.get_first_price_by_symbol_by_year(profile.Symbol,
                                                                                         "1402").replace(",", "")

                    row["currency_name"] = currency
                    row["year_1400"] = float(price1400)
                    row["year_1401"] = float(price1401)
                    row["year_1402"] = float(price1402)
                    row["daily_price"] = float(priceCurrent)

                elif key == "cbi":
                    inflationRateYearlyService = InflationRateYearlyService()
                    inf1400 = inflationRateYearlyService.get_inflation_rate_yearly_by_year("1400")
                    inf1401 = inflationRateYearlyService.get_inflation_rate_yearly_by_year("1401")

                    row["currency_name"] = currency
                    row["year_1400"] = float(inf1400.InflationRate)
                    row["year_1401"] = float(inf1401.InflationRate)
                    row["year_1402"] = ""
                    row["daily_price"] = ""

                elif key == "ime":
                    physicalTransactionService = PhysicalTransactionService()
                    trans1400 = physicalTransactionService.calc_weighted_average_GoodsName_by_year(
                        currency,
                        "1400")
                    trans1401 = physicalTransactionService.calc_weighted_average_GoodsName_by_year(
                        currency,
                        "1401")
                    trans1402 = physicalTransactionService.calc_weighted_average_GoodsName_by_year(
                        currency,
                        "1402")

                    row["currency_name"] = currency

                    row["year_1400"] = float(trans1400)
                    row["year_1401"] = float(trans1401)
                    row["year_1402"] = float(trans1402)

                elif key == "tradingeconomics":
                    ProfileHistoryService = ProfilesHistoryService()
                    price1400 = ProfileHistoryService.get_first_price_by_AnnId_and_year(currency, "2021")
                    price1401 = ProfileHistoryService.get_first_price_by_AnnId_and_year(currency, "2022")
                    price1402 = ProfileHistoryService.get_first_price_by_AnnId_and_year(currency, "2023")
                    lastPrice = ProfileHistoryService.get_last_price_by_AnnId(currency)

                    row["currency_name"] = etp_column_maps[currency]
                    row["year_1400"] = float(price1400)
                    row["year_1401"] = float(price1401)
                    row["year_1402"] = float(price1402)
                    row["daily_price"] = float(lastPrice)

                rows.append(row)

        for element in rows:
            price_table_service.update_price_table(element)
