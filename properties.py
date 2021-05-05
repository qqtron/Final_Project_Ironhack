import pandas as pd


class Property:

    RENOVATION_COST_PRICES = {1:50, 2:66, 3:83, 4:100}
    CADASTRAL_MODIFIER = 0.4
    MUNICIPAL_TAX_MODIFIER = 0.00479
    PRICE_DATASET = None
    MANAGEMENT_FEE = 0
    AVG_COMMUNITY_COSTS = 150

    def __init__(self, zone, bedrooms, acquisition_price):
        self.bedrooms = bedrooms
        self.zone = zone
        self.acquisition_price = acquisition_price
        self.municipal_tax = (self.acquisition_price * Property.CADASTRAL_MODIFIER * Property.MUNICIPAL_TAX_MODIFIER) / 12
        self.renovation_cost = Property.RENOVATION_COST_PRICES[self.bedrooms]
        self.community_cost = Property.AVG_COMMUNITY_COSTS
        self.internet_price = 0
        self.price_dataset = Property.PRICE_DATASET
        self.management_fee = Property.MANAGEMENT_FEE

    @property
    def investment(self):
        investment_costs = [self.acquisition_price, self.decoration_price, self.equipment_price]
        return sum(investment_costs)

    @property
    def opex(self):
        opex_costs = [self.utilities_price, self.hotelery_price,
                      self.internet_price, self.municipal_tax, self.renovation_cost, self.community_cost]
        return sum(opex_costs) + (self.management_fee * self.average_rental_price)

    @property
    def noi(self):
        return (self.average_rental_price * self.avg_occupancy) - self.opex

    @property
    def profitability(self):
        return ((self.noi * 12) / self.investment) * 100

    def __repr__(self):
        return f"""

# {self.__class__.__name__.replace('Property', '')}
---------------------------------------------------
## Investment
- Acquisition price: {self.acquisition_price:,.2f} €
- Decoration investment: {self.decoration_price:,.2f} €
- Equipment investment: {self.equipment_price:,.2f} €

## Predicted income
- Average rental price: {self.average_rental_price:,.2f} €
- OPEX: {self.opex:,.2f} €
- NOI: {self.noi:,.2f} €

## Profitability
*{self.profitability:,.2f} %*
"""

class CorporateProperty(Property):

    RENOVATION_COST_PRICES = {1:50, 2:66, 3:83, 4:100}
    UTILITIES_PRICES = {1:120, 2:150, 3:170, 4:200}
    DECORATION_PRICES = {1:12000, 2:14000, 3:17000, 4:20000}
    EQUIPMENT_PRICES = {1:1200, 2:1400, 3:1700, 4:2000}
    HOTELERY_PRICES = {1:108, 2:150, 3:220, 4:280}
    INTERNET_PRICE = 50
    PRICE_DATASET = 'datasets/rental_prices_corporate.xlsx'
    PRICE_DATASET_ZONE_COLUMN = 'LOCATIONNAME'
    PRICE_DATASET_ROOMS_COLUMN = 'ROOMS'
    PRICE_DATASET_PRICE_COLUMN = 'PRECIO'
    MANAGEMENT_FEE = 0.1
    AVG_OCCUPANCY = 0.85

    def __init__(self, zone, bedrooms, acquisition_price):
        super().__init__(zone, bedrooms, acquisition_price)
        self.decoration_price = CorporateProperty.DECORATION_PRICES[self.bedrooms]
        self.equipment_price = CorporateProperty.EQUIPMENT_PRICES[self.bedrooms]
        self.utilities_price = CorporateProperty.UTILITIES_PRICES[self.bedrooms]
        self.hotelery_price = CorporateProperty.HOTELERY_PRICES[self.bedrooms]
        self.internet_price = CorporateProperty.INTERNET_PRICE
        self.management_fee = CorporateProperty.MANAGEMENT_FEE
        self.avg_occupancy = CorporateProperty.AVG_OCCUPANCY

    @classmethod
    def zones(self):
        df = pd.read_excel(CorporateProperty.PRICE_DATASET)
        return df[CorporateProperty.PRICE_DATASET_ZONE_COLUMN].unique()

    @property
    def average_rental_price(self):
        df = pd.read_excel(CorporateProperty.PRICE_DATASET)

        # Filter dataset by number of rooms
        df = df[df[CorporateProperty.PRICE_DATASET_ROOMS_COLUMN].isin([self.bedrooms])]

        # Filter dataset by zone
        df = df[df[CorporateProperty.PRICE_DATASET_ZONE_COLUMN].isin([self.zone])]

        # Get average price
        return df[CorporateProperty.PRICE_DATASET_PRICE_COLUMN].mean()


class TouristProperty(Property):

    RENOVATION_COST_PRICES = {1:50, 2:66, 3:83, 4:100}
    UTILITIES_PRICES = {1:120, 2:150, 3:170, 4:200}
    DECORATION_PRICES = {1:12000, 2:14000, 3:17000, 4:20000}
    EQUIPMENT_PRICES = {1:1200, 2:1400, 3:1700, 4:2000}
    HOTELERY_PRICES = {1:108, 2:150, 3:220, 4:280}
    INTERNET_PRICE = 50
    PRICE_DATASET = 'datasets/rental_prices_tourist.csv'
    PRICE_DATASET_ZONE_COLUMN = 'LOCATION'
    PRICE_DATASET_ROOMS_COLUMN = 'ROOMS'
    PRICE_DATASET_DAILY_RATE_COLUMN = 'Avg. Daily Rate'
    PRICE_DATASET_OCCUPANCY_RATE_COLUMN = 'Occupancy Rate'
    MANAGEMENT_FEE = 0.16
    AIRBNB_FEE = 0.14


    def __init__(self, zone, bedrooms, acquisition_price):
        super().__init__(zone, bedrooms, acquisition_price)
        self.decoration_price = TouristProperty.DECORATION_PRICES[self.bedrooms]
        self.equipment_price = TouristProperty.EQUIPMENT_PRICES[self.bedrooms]
        self.utilities_price = TouristProperty.UTILITIES_PRICES[self.bedrooms]
        self.hotelery_price = TouristProperty.HOTELERY_PRICES[self.bedrooms]
        self.internet_price = TouristProperty.INTERNET_PRICE
        self.management_fee = TouristProperty.MANAGEMENT_FEE
        self.airbnb_fee = TouristProperty.AIRBNB_FEE


    @classmethod
    def zones(self):
        df = pd.read_csv(TouristProperty.PRICE_DATASET)
        return df[TouristProperty.PRICE_DATASET_ZONE_COLUMN].unique()

    @property
    def average_rental_price(self):
        df = pd.read_csv(TouristProperty.PRICE_DATASET)

        # Filter dataset by number of rooms
        df = df[df[TouristProperty.PRICE_DATASET_ROOMS_COLUMN].isin([self.bedrooms])]

        # Filter dataset by zone
        df = df[df[TouristProperty.PRICE_DATASET_ZONE_COLUMN].isin([self.zone])]

        # Get average price
        return (df[TouristProperty.PRICE_DATASET_DAILY_RATE_COLUMN].mean() * 30)* df[TouristProperty.PRICE_DATASET_OCCUPANCY_RATE_COLUMN].mean()

    @property
    def avg_occupancy(self):
        df = pd.read_csv(TouristProperty.PRICE_DATASET)

        # Filter dataset by number of rooms
        df = df[df[TouristProperty.PRICE_DATASET_ROOMS_COLUMN].isin([self.bedrooms])]

        # Filter dataset by zone
        df = df[df[TouristProperty.PRICE_DATASET_ZONE_COLUMN].isin([self.zone])]

        # Get average occupancy
        return df[TouristProperty.PRICE_DATASET_OCCUPANCY_RATE_COLUMN].mean()

    @property
    def opex(self):
        opex_costs = [self.utilities_price,
                      self.internet_price, self.municipal_tax, self.renovation_cost, self.community_cost]
        return sum(opex_costs) + (self.management_fee * self.airbnb_fee * self.average_rental_price)

    @property
    def noi(self):
        return self.average_rental_price - self.opex


class TraditionalProperty(Property):

    RENOVATION_COST_PRICES = {1:50, 2:66, 3:83, 4:100}
    UTILITIES_PRICES = {1:120, 2:150, 3:170, 4:200}
    DECORATION_PRICES = {1:12000, 2:14000, 3:17000, 4:20000}
    EQUIPMENT_PRICES = {1:1200, 2:1400, 3:1700, 4:2000}
    HOTELERY_PRICES = {1:108, 2:150, 3:220, 4:280}
    INTERNET_PRICE = 50
    PRICE_DATASET = 'datasets/rental_prices_traditional.csv'
    PRICE_DATASET_ZONE_COLUMN = 'LOCATIONNAME'
    PRICE_DATASET_ROOMS_COLUMN = 'ROOMS'
    PRICE_DATASET_PRICE_COLUMN = 'PRICE_ASKING'
    MANAGEMENT_FEE = 1
    AVG_OCCUPANCY = 1


    def __init__(self, zone, bedrooms, acquisition_price):
        super().__init__(zone, bedrooms, acquisition_price)
        self.decoration_price = TraditionalProperty.DECORATION_PRICES[self.bedrooms]
        self.equipment_price = TraditionalProperty.EQUIPMENT_PRICES[self.bedrooms]
        self.utilities_price = TraditionalProperty.UTILITIES_PRICES[self.bedrooms]
        self.hotelery_price = TraditionalProperty.HOTELERY_PRICES[self.bedrooms]
        self.internet_price = TraditionalProperty.INTERNET_PRICE
        self.management_fee = TraditionalProperty.MANAGEMENT_FEE
        self.avg_occupancy = TraditionalProperty.AVG_OCCUPANCY

    @classmethod
    def zones(cls):
        df = pd.read_csv(cls.PRICE_DATASET)
        return df[cls.PRICE_DATASET_ZONE_COLUMN].unique()

    @property
    def average_rental_price(self):
        df = pd.read_csv(TraditionalProperty.PRICE_DATASET)

        # Filter dataset by number of rooms
        df = df[df[TraditionalProperty.PRICE_DATASET_ROOMS_COLUMN].isin([self.bedrooms])]

        # Filter dataset by zone
        df = df[df[TraditionalProperty.PRICE_DATASET_ZONE_COLUMN].isin([self.zone])]

        # Get average price
        return df[TraditionalProperty.PRICE_DATASET_PRICE_COLUMN].mean()

    @property
    def opex(self):
        opex_costs = [self.municipal_tax, self.renovation_cost, self.community_cost]
        return sum(opex_costs)


