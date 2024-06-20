from sqlalchemy import inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.instrument_info import InstrumentInfo

Base = declarative_base()


class InstrumentInfoDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the InstrumentInfoDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_instrument_info(self, data):
        """
        Saves a new instrument info entry.

        Parameters:
        - data (dict): Dictionary containing instrument info data.

        Returns:
        - int: Saved instrument info entry's ID
        """
        instrument_info = InstrumentInfo(**data)
        self.session.add(instrument_info)
        self.session.commit()
        self.logger.info(f"Saved instrument info entry with ID: {instrument_info.insCode}")
        return instrument_info.insCode

    def get_all_instrument_info_entries(self):
        """
        Retrieves all instrument info entries.

        Returns:
        - list: List of all instrument info entries.
        """
        return self.session.query(InstrumentInfo).all()

    def get_instrument_info_by_id(self, insCode):
        """
        Retrieves an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.session.query(InstrumentInfo).filter_by(insCode=insCode).first()

    def update_instrument_info(self, data):
        """
        Updates an instrument info entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated instrument info entry's ID
        """

        existing_record = self.get_instrument_info_by_id(data.get("insCode"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            self.logger.info(f"Updated instrument info entry with ID: {existing_record.lVal18AFC}")
            return existing_record.insCode

        else:
            return self.save_instrument_info(data)

    def delete_instrument_info_by_id(self, insCode):
        """
        Deletes an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        instrument_info = self.session.query(InstrumentInfo).filter_by(insCode=insCode).first()
        if instrument_info:
            self.session.delete(instrument_info)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the instrument_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(InstrumentInfo.__tablename__)

    def create_table(self):
        """
        Create the tse_instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                InstrumentInfo.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_insCodes_englishName_persianName(self, ):
        """
        Retrieves insCode values, along with English and Persian names, for a given marketName using the stored procedure.

        Parameters:
        - marketName (str): The marketName to query.

        Returns:
        - list of dicts: List of dictionaries containing insCode, EnglishName, and PersianName.
        """
        # Define the stored procedure call with a parameter for marketName
        sp_call = text("EXEC GetInsCodesAndEnglishAndPersianNames")

        # Execute the stored procedure with the marketName parameter and fetch the result
        result = self.session.execute(sp_call, {})

        # Extract insCode, EnglishName, and PersianName values from the result
        insCodes_info = [{"insCode": row[0], "PersianName": row[1], "EnglishName": row[2]} for row in result]

        return insCodes_info

    def get_all_persian_symbols(self):
        """
        Retrieves all values in the lVal18AFC column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the lVal18AFC column.
        """
        # lVal18AFC_values = self.session.query(InstrumentInfo.lVal18AFC).filter_by(flow="1").all()
        # return [value[0] for value in lVal18AFC_values]
        iranian_companies = [
            "آباد",
            "آبادا",
            "آپ",
            "آريا",
            "آسيا",
            "اپال",
            "اپرداز",
            "اتكام",
            "اتكاي",
            "اخابر",
            "ارفع",
            "اسياتك",
            "اعتلا",
            "افرا",
            "افق",
            "اميد",
            "امين",
            "انتخاب",
            "انرژي",
            "اوان",
            "بالبر",
            "بپاس",
            "بپيوند",
            "بترانس",
            "بجهرم",
            "بخاور",
            "بركت",
            "بزاگرس",
            "بساما",
            "بسويچ",
            "بشهاب",
            "بفجر",
            "بكابل",
            "بكام",
            "بكهنوج",
            "بگيلان",
            "بمپنا",
            "بموتو",
            "بمولد",
            "بنو",
            "بنيرو",
            "بورس",
            "بوعلي",
            "پارتا",
            "پارسان",
            "پارسيان",
            "پاسا",
            "پاكشو",
            "پتاير",
            "پترول",
            "پخش",
            "پدرخش",
            "پرديس",
            "پسهند",
            "پكرمان",
            "پكوير",
            "پلاسك",
            "پي پاد",
            "پيزد",
            "تاپكيش",
            "تاپيكو",
            "تاصيكو",
            "تايرا",
            "تبرك",
            "تپسي",
            "تپمپي",
            "تجلي",
            "تكاردان",
            "تكشا",
            "تكمبا",
            "تكنو",
            "تليسه",
            "تماوند",
            "تملت",
            "تنوين",
            "توريل",
            "توسن",
            "تيپيكو",
            "ثاخت",
            "ثالوند",
            "ثامان",
            "ثاميد",
            "ثباغ",
            "ثبهساز",
            "ثپرديس",
            "ثتران",
            "ثجنوب",
            "ثرود",
            "ثشاهد",
            "ثشرق",
            "ثعمرا",
            "ثغرب",
            "ثمسكن",
            "ثنوسا",
            "جم",
            "جم پيلن",
            "چافست",
            "چخزر",
            "چدن",
            "چفيبر",
            "چكاپا",
            "چكارن",
            "چكاوه",
            "حآسا",
            "حپارسا",
            "حپترو",
            "حپرتو",
            "حتايد",
            "حتوكا",
            "حخزر",
            "حريل",
            "حسير",
            "حسينا",
            "حفارس",
            "حفاري",
            "حكشتي",
            "حگهر",
            "خاذين",
            "خاهن",
            "خاور",
            "خپويش",
            "ختراك",
            "ختور",
            "ختوقا",
            "خچرخش",
            "خديزل",
            "خراسان",
            "خريخت",
            "خرينگ",
            "خزاميا",
            "خزر",
            "خساپا",
            "خشرق",
            "خفنر",
            "خكرمان",
            "خكمك",
            "خگستر",
            "خلنت",
            "خمحركه",
            "خمحور",
            "خمهر",
            "خموتور",
            "خنصير",
            "خودرو",
            "خوساز",
            "دابور",
            "دارو",
            "داسوه",
            "دالبر",
            "دامين",
            "دانا",
            "داوه",
            "دبالك",
            "دپارس",
            "دتماد",
            "دتوزيع",
            "دتوليد",
            "دجابر",
            "ددام",
            "ددانا",
            "درازك",
            "درازي",
            "درهآور",
            "دروز",
            "دزهراوي",
            "دسبحا",
            "دسبحان",
            "دسينا",
            "دشيمي",
            "دعبيد",
            "دفارا",
            "دفرا",
            "دقاضي",
            "دكپسول",
            "دكوثر",
            "دكيمي",
            "دلر",
            "دلقما",
            "دماوند",
            "ديران",
            "ذوب",
            "رافزا",
            "رانفور",
            "رتاپ",
            "ركيش",
            "رمپنا",
            "رنيك",
            "ريشمك",
            "زاگرس",
            "زبينا",
            "زپارس",
            "زدشت",
            "زشريف",
            "زشگزا",
            "زفجر",
            "زفكا",
            "زقيام",
            "زكشت",
            "زكوثر",
            "زگلدشت",
            "زماهان",
            "زمگسا",
            "زملارد",
            "زنگان",
            "سآبيك",
            "ساراب",
            "ساربيل",
            "ساروج",
            "ساروم",
            "سامان",
            "ساوه",
            "ساينا",
            "سبجنو",
            "سبزوا",
            "سبهان",
            "سپ",
            "سپاها",
            "سپيدار",
            "ستران",
            "سجام",
            "سخزر",
            "سخوز",
            "سدبير",
            "سدشت",
            "سدور",
            "سرچشمه",
            "سرود",
            "سشرق",
            "سشمال",
            "سصفها",
            "سصوفي",
            "سغدير",
            "سغرب",
            "سفار",
            "سفارس",
            "سفانو",
            "سقاين",
            "سكرد",
            "سكرما",
            "سمازن",
            "سمگا",
            "سنير",
            "سهرمز",
            "سهگمت",
            "سيدكو",
            "سيستم",
            "سيلام",
            "سيمرغ",
            "شاراك",
            "شاروم",
            "شاملا",
            "شاوان",
            "شبريز",
            "شبصير",
            "شبندر",
            "شبهرن",
            "شپارس",
            "شپاس",
            "شپاكسا",
            "شپنا",
            "شتران",
            "شتوكا",
            "شجم",
            "شخارك",
            "شدوص",
            "شراز",
            "شرانل",
            "شسپا",
            "شستا",
            "شسينا",
            "شصدف",
            "شغدير",
            "شفا",
            "شفارس",
            "شفن",
            "شكام",
            "شكربن",
            "شكلر",
            "شگل",
            "شگويا",
            "شلعاب",
            "شملي",
            "شنفت",
            "شهر",
            "شوينده",
            "شيراز",
            "شيران",
            "صبا",
            "عاليس",
            "غاذر",
            "غالبر",
            "غبشهر",
            "غبهنوش",
            "غپآذر",
            "غپاك",
            "غپونه",
            "غپينو",
            "غچين",
            "غدام",
            "غدانه",
            "غدشت",
            "غديس",
            "غزر",
            "غسالم",
            "غشاذر",
            "غشان",
            "غشصفا",
            "غشهد",
            "غشهداب",
            "غصينو",
            "غفارس",
            "غكورش",
            "غگرجي",
            "غگل",
            "غگلپا",
            "غگلستا",
            "غمايه",
            "غمهرا",
            "غمينو",
            "غنوش",
            "غويتا",
            "فاذر",
            "فاراك",
            "فارس",
            "فاسمين",
            "فايرا",
            "فباهنر",
            "فپنتا",
            "فتوسا",
            "فجام",
            "فجهان",
            "فخاس",
            "فخوز",
            "فرآور",
            "فرابورس",
            "فرود",
            "فروژ",
            "فروس",
            "فروسيل",
            "فروي",
            "فزر",
            "فزرين",
            "فسبزوار",
            "فسپا",
            "فسرب",
            "فسوژ",
            "فصبا",
            "فغدير",
            "فگستر",
            "فلامي",
            "فلوله",
            "فمراد",
            "فملي",
            "فن افزار",
            "فنورد",
            "فولاد",
            "فولاژ",
            "فولاي",
            "قاسم",
            "قپيرا",
            "قثابت",
            "قچار",
            "قرن",
            "قزوين",
            "قشكر",
            "قشهد",
            "قشير",
            "قصفها",
            "قلرست",
            "قمرو",
            "قهكمت",
            "كاذر",
            "كاسپين",
            "كالا",
            "كاما",
            "كاوه",
            "كبافق",
            "كپارس",
            "كپرور",
            "كپشير",
            "كترام",
            "كتوسعه",
            "كتوكا",
            "كچاد",
            "كحافظ",
            "كخاك",
            "كدما",
            "كرازي",
            "كرماشا",
            "كرمان",
            "كروميت",
            "كروي",
            "كزغال",
            "كساپا",
            "كساوه",
            "كسرا",
            "كسعدي",
            "كشرق",
            "كطبس",
            "كفپارس",
            "كفرا",
            "كگاز",
            "كگل",
            "كگهر",
            "كلوند",
            "كماسه",
            "كمنگنز",
            "كنور",
            "كهمدا",
            "كي بي سي",
            "كيميا",
            "كيمياتك",
            "گدنا",
            "گكوثر",
            "گلديرا",
            "گوهران",
            "لبوتان",
            "لپارس",
            "لخزر",
            "لطيف",
            "لوتوس",
            "ما",
            "ماديرا",
            "مارون",
            "مبين",
            "مداران",
            "مديريت",
            "مفاخر",
            "ملت",
            "ميدكو",
            "ميهن",
            "ناما",
            "نطرين",
            "نمرينو",
            "نوري",
            "نوين",
            "نيان",
            "هاي وب",
            "هجرت",
            "هرمز",
            "همراه",
            "وآذر",
            "وآفري",
            "وآوا",
            "واتي",
            "واحيا",
            "واعتبار",
            "والبر",
            "والماس",
            "واميد",
            "وامين",
            "وبانك",
            "وبهمن",
            "وبوعلي",
            "وبيمه",
            "وپارس",
            "وپاسار",
            "وپترو",
            "وپخش",
            "وپست",
            "وپويا",
            "وتجارت",
            "وتعاون",
            "وتوس",
            "وتوسم",
            "وتوشه",
            "وتوصا",
            "وتوكا",
            "وخارزم",
            "وخاور",
            "ودي",
            "ورنا",
            "وساپا",
            "وساخت",
            "وسبحان",
            "وسپه",
            "وسپهر",
            "وسكاب",
            "وسينا",
            "وصنا",
            "وصندوق",
            "وصنعت",
            "وطوبي",
            "وغدير",
            "وكار",
            "وكبهمن",
            "وكغدير",
            "وگردش",
            "وگستر",
            "ولبهمن",
            "ولپارس",
            "ولساپا",
            "ولشرق",
            "ولصنم",
            "ولغدر",
            "ولكار",
            "ولملت",
            "ومعادن",
            "وملل",
            "ومهان",
            "ونفت",
            "ونوين",
            "ونيكي",
            "وهامون",
            "وهور"
        ]
        return iranian_companies

    def get_all_ins_codes(self):
        """
        Retrieves all values in the insCode column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the insCode column.
        """
        insCode_values = self.session.query(InstrumentInfo.insCode).all()
        return [value[0] for value in insCode_values]

    def get_all_persian_symbols_by_sector_code(self, value):
        """
        Retrieves all values in the lVal18AFC column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the lVal18AFC column.
        """
        instrumentInfo = self.session.query(InstrumentInfo).filter_by(cSecVal=value).all()
        return [inst.lVal18AFC for inst in instrumentInfo]

    def get_instrument_info_by_persian_symbol(self, symbolFa):
        """
        Retrieves an instrument info entry by its symbol.

        Parameters:
        - insCode (str): Instrument info entry symbol to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.session.query(InstrumentInfo).filter_by(lVal18AFC=symbolFa).first()

    def get_list_data(self, inscode):

        result = []
        data = self.get_instrument_info_by_id(inscode)

        result.append(data.psGelStaMax)
        result.append(data.psGelStaMin)
        result.append(data.zTitad)
        result.append(data.baseVol)
        result.append(data.kAjCapValCpsIdx)
        result.append(data.qTotTran5JAvg)
        result.append(data.estimatedEPS)

        return result
