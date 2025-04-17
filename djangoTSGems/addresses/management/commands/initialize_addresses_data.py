# from django.core.management.base import BaseCommand
# from djangoTSGems.addresses.models.country import Country
# from djangoTSGems.addresses.models.city import City
# from djangoTSGems.addresses.models.postal_code import PostalCode
# from djangoTSGems.addresses.models.street_address import StreetAddress
# from faker import Faker
# from faker.config import AVAILABLE_LOCALES


# european_countries = {
#     'Albania': 'en_GB',
#     'Andorra': 'es_ES',
#     'Austria': 'de_AT',
#     'Belarus': 'ru_RU',
#     'Belgium': 'nl_BE',
#     'Bosnia and Herzegovina': 'hr_HR',
#     'Bulgaria': 'bg_BG',
#     'Croatia': 'hr_HR',
#     'Cyprus': 'el_GR',
#     'Czech Republic': 'cs_CZ',
#     'Denmark': 'da_DK',
#     'Estonia': 'en_GB',
#     'Finland': 'fi_FI',
#     'France': 'fr_FR',
#     'Germany': 'de_DE',
#     'Greece': 'el_GR',
#     'Hungary': 'hu_HU',
#     'Iceland': 'is_IS',
#     'Ireland': 'en_IE',
#     'Italy': 'it_IT',
#     'Kosovo': 'en_GB',
#     'Latvia': 'en_GB',
#     'Liechtenstein': 'de_CH',
#     'Lithuania': 'en_GB',
#     'Luxembourg': 'fr_FR',
#     'Malta': 'en_GB',
#     'Moldova': 'ro_MD',
#     'Monaco': 'fr_FR',
#     'Montenegro': 'hr_HR',
#     'Netherlands': 'nl_NL',
#     'North Macedonia': 'hr_HR',
#     'Norway': 'no_NO',
#     'Poland': 'pl_PL',
#     'Portugal': 'pt_PT',
#     'Romania': 'ro_RO',
#     'San Marino': 'it_IT',
#     'Serbia': 'sr_RS',
#     'Slovakia': 'sk_SK',
#     'Slovenia': 'sl_SI',
#     'Spain': 'es_ES',
#     'Sweden': 'sv_SE',
#     'Switzerland': 'de_CH',
#     'Ukraine': 'uk_UA',
#     'Vatican City': 'it_IT'
# }


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         fake = Faker()

#         for country_name, locale in european_countries.items():
#             if locale not in AVAILABLE_LOCALES:
#                 locale = 'en_GB'

#             country = Country.objects.create(name=country_name)

#             fake = Faker(locale)

#             for _ in range(20):
#                 city_name = fake.city()

#                 city = City.objects.create(name=city_name, country=country)

#                 for _ in range(20):

#                     postal_code = fake.postcode()

#                     postal_code = PostalCode.objects.create(
#                         code=postal_code, city=city)

#                     for _ in range(20):
#                         street = fake.street_address()

#                         StreetAddress.objects.create(
#                             street_address=street, postal_code=postal_code)

#             self.stdout.write(self.style.SUCCESS(
#                 f'Successfully created data for {country_name}'))


# from django.core.management.base import BaseCommand
# from djangoTSGems.addresses.models.country import Country
# from djangoTSGems.addresses.models.city import City
# from djangoTSGems.addresses.models.postal_code import PostalCode
# from djangoTSGems.addresses.models.street_address import StreetAddress
# from mimesis import Generic

# european_countries = {
#     'Albania': 'en',  # Mimesis uses generic English for Albania
#     'Andorra': 'es',  # Mimesis uses Spanish for Andorra
#     'Austria': 'de',  # Mimesis uses German for Austria
#     'Belarus': 'ru',  # Mimesis uses Russian for Belarus
#     'Belgium': 'nl',  # Mimesis uses Dutch for Belgium
#     'Bosnia and Herzegovina': 'hr',  # Mimesis uses Croatian for Bosnia
#     'Bulgaria': 'ru',  # Mimesis uses Bulgarian for Bulgaria
#     'Croatia': 'hr',  # Mimesis uses Croatian for Croatia
#     'Cyprus': 'el',  # Mimesis uses Greek for Cyprus
#     'Czech Republic': 'cs',  # Mimesis uses Czech for Czech Republic
#     'Denmark': 'da',  # Mimesis uses Danish for Denmark
#     'Estonia': 'et',  # Mimesis uses Estonian for Estonia
#     'Finland': 'fi',  # Mimesis uses Finnish for Finland
#     'France': 'fr',  # Mimesis uses French for France
#     'Germany': 'de',  # Mimesis uses German for Germany
#     'Greece': 'el',  # Mimesis uses Greek for Greece
#     'Hungary': 'hu',  # Mimesis uses Hungarian for Hungary
#     'Iceland': 'is',  # Mimesis uses Icelandic for Iceland
#     'Ireland': 'en',  # Mimesis uses English for Ireland
#     'Italy': 'it',  # Mimesis uses Italian for Italy
#     'Kosovo': 'sq',  # Mimesis uses Albanian for Kosovo
#     'Latvia': 'lv',  # Mimesis uses Latvian for Latvia
#     'Liechtenstein': 'de',  # Mimesis uses German for Liechtenstein
#     'Lithuania': 'lt',  # Mimesis uses Lithuanian for Lithuania
#     'Luxembourg': 'fr',  # Mimesis uses French for Luxembourg
#     'Malta': 'mt',  # Mimesis uses Maltese for Malta
#     'Moldova': 'ro',  # Mimesis uses Romanian for Moldova
#     'Monaco': 'fr',  # Mimesis uses French for Monaco
#     'Montenegro': 'sr',  # Mimesis uses Serbian for Montenegro
#     'Netherlands': 'nl',  # Mimesis uses Dutch for Netherlands
#     'North Macedonia': 'mk',  # Mimesis uses Macedonian for North Macedonia
#     'Norway': 'no',  # Mimesis uses Norwegian for Norway
#     'Poland': 'pl',  # Mimesis uses Polish for Poland
#     'Portugal': 'pt',  # Mimesis uses Portuguese for Portugal
#     'Romania': 'ro',  # Mimesis uses Romanian for Romania
#     'San Marino': 'it',  # Mimesis uses Italian for San Marino
#     'Serbia': 'sr',  # Mimesis uses Serbian for Serbia
#     'Slovakia': 'sk',  # Mimesis uses Slovak for Slovakia
#     'Slovenia': 'sl',  # Mimesis uses Slovenian for Slovenia
#     'Spain': 'es',  # Mimesis uses Spanish for Spain
#     'Sweden': 'sv',  # Mimesis uses Swedish for Sweden
#     'Switzerland': 'de',  # Mimesis uses German for Switzerland
#     'Ukraine': 'uk',  # Mimesis uses Ukrainian for Ukraine
#     'Vatican City': 'it',  # Mimesis uses Italian for Vatican City
# }



# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         # Iterate through the list of countries and locales
#         for country_name, locale in european_countries.items():
#             # Instantiate Mimesis' Generic class with the given locale
#             generic = Generic(locale)

#             # Create the country entry in the database
#             country = Country.objects.create(name=country_name)

#             # Generate 20 cities for each country
#             for _ in range(10):
#                 city_name = generic.address.city()  # Generate a city for the locale
#                 city = City.objects.create(name=city_name, country=country)

#                 # Generate 20 postal codes for each city
#                 for _ in range(10):
#                     postal_code = generic.address.zip_code()  # Generate a postal code for the city
#                     postal_code = PostalCode.objects.create(code=postal_code, city=city)

#                     # Generate 20 street addresses for each postal code
#                     for _ in range(10):
#                         street_address = generic.address.address()  # Generate a street address
#                         StreetAddress.objects.create(street_address=street_address, postal_code=postal_code)

#             # Output success message for each country
#             self.stdout.write(self.style.SUCCESS(
#                 f'Successfully created data for {country_name}'))


# import requests
# from django.core.management.base import BaseCommand
# from djangoTSGems.addresses.models.country import Country
# from djangoTSGems.addresses.models.city import City
# from djangoTSGems.addresses.models.postal_code import PostalCode
# from djangoTSGems.addresses.models.street_address import StreetAddress

# class Command(BaseCommand):
#     help = 'Populate the database with European countries, cities, postal codes, and street addresses'

#     # Define European countries to fetch data for
#     european_countries = [
#         'Albania', 'Andorra', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',
#         'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
#         'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
#         'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Netherlands', 'Norway', 'Poland',
#         'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
#         'Sweden', 'Switzerland', 'Ukraine', 'Vatican City'
#     ]

#     def handle(self, *args, **kwargs):
#         geonames_username = 'beatrisilieva'  # Replace with your GeoNames username

#         # Loop through each European country
#         for country_name in self.european_countries:
#             # Get the country code using GeoNames API
#             country_url = f"http://api.geonames.org/searchJSON?q={country_name}&maxRows=1&username={geonames_username}"
#             response = requests.get(country_url)
#             data = response.json()

#             if data['geonames']:
#                 country_code = data['geonames'][0]['countryCode']
#                 # Create country in the database
#                 country = Country.objects.create(name=country_name)

#                 # Fetch cities for the country
#                 cities_url = f"http://api.geonames.org/searchJSON?country={country_code}&maxRows=50&username={geonames_username}"
#                 cities_response = requests.get(cities_url)
#                 cities_data = cities_response.json()

#                 for city_data in cities_data['geonames']:
#                     city_name = city_data['name']
#                     city = City.objects.create(name=city_name, country=country)

#                     # Fetch postal codes for the city
#                     postal_codes_url = f"http://api.geonames.org/searchJSON?city={city_name}&country={country_code}&maxRows=10&username={geonames_username}"
#                     postal_codes_response = requests.get(postal_codes_url)
#                     postal_codes_data = postal_codes_response.json()

#                     for postal_data in postal_codes_data['geonames']:
#                         postal_code = postal_data.get('postalcode')  # Use .get() to avoid KeyError
#                         if postal_code:
#                             postal_code_obj = PostalCode.objects.create(code=postal_code, city=city)
#                             street_address = f"{postal_code} Example Street"
#                             StreetAddress.objects.create(street_address=street_address, postal_code=postal_code_obj)
#                         else:
#                             self.stdout.write(self.style.WARNING(f"No postal code found for {city_name}."))

#                 self.stdout.write(self.style.SUCCESS(f'Successfully populated data for {country_name}'))

#         self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))




# from django.core.management.base import BaseCommand
# from faker import Faker

# from cities_light.models import Country, City
# from djangoTSGems.addresses.models.postal_code import PostalCode
# from djangoTSGems.addresses.models.street_address import StreetAddress

# fake = Faker()

# EUROPEAN_COUNTRY_CODES = [
#     'AL', 'AD', 'AM', 'AT', 'AZ', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
#     'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'XK', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC',
#     'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR',
#     'UA', 'GB', 'VA'
# ]

# class Command(BaseCommand):
#     help = "Generate postal codes and street addresses for European cities only"

#     def handle(self, *args, **kwargs):
#         europe_countries = Country.objects.filter(code2__in=EUROPEAN_COUNTRY_CODES)
#         self.stdout.write(f"Found {europe_countries.count()} European countries.")

#         city_qs = City.objects.filter(country__in=europe_countries)

#         count_postal = 0
#         count_addresses = 0

#         for city in city_qs:
#             for _ in range(3): 
#                 code = fake.postcode()
#                 postal_code = PostalCode.objects.create(code=code, city=city)
#                 count_postal += 1

#                 for _ in range(3):  
#                     street = fake.street_address()
#                     StreetAddress.objects.create(street_address=street, postal_code=postal_code)
#                     count_addresses += 1

#         self.stdout.write(self.style.SUCCESS(f"Created {count_postal} postal codes and {count_addresses} addresses."))


import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from djangoTSGems.addresses.models.state import State
from djangoTSGems.addresses.models.city import City
from djangoTSGems.addresses.models.zip_code import ZipCode
from djangoTSGems.addresses.models.street_address import StreetAddress

fake = Faker()

# List of 50 US States
states_list = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
    'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
    'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

class Command(BaseCommand):
    help = 'Generate fake data for US states, cities, zip codes, and street addresses.'

    def handle(self, *args, **kwargs):
        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Create States from the list of actual US states
            states = []
            for state_name in states_list:
                state, created = State.objects.get_or_create(name=state_name)
                if created:
                    states.append(state)
            
            self.stdout.write(self.style.SUCCESS(f"Created {len(states)} states."))

            # Create Cities and ZipCodes
            for state in states:
                # Generate a random number of cities per state
                num_cities = random.randint(3, 10)
                for _ in range(num_cities):
                    city_name = fake.city()
                    city, created = City.objects.get_or_create(name=city_name, state=state)
                    if created:
                        # Generate ZipCodes for each city
                        num_zip_codes = random.randint(1, 3)
                        for _ in range(num_zip_codes):
                            zip_code = fake.zipcode()
                            zip_code_obj, created = ZipCode.objects.get_or_create(code=zip_code, city=city)
                            if created:
                                # Generate Street Addresses for each ZipCode
                                num_streets = random.randint(2, 5)
                                for _ in range(num_streets):
                                    street_address = fake.street_address()
                                    street_address_obj = StreetAddress.objects.create(
                                        street_address=street_address,
                                        zip_code=zip_code_obj
                                    )
                                self.stdout.write(self.style.SUCCESS(f"Created {num_streets} street addresses for {zip_code_obj}"))
                    self.stdout.write(self.style.SUCCESS(f"Created {num_zip_codes} zip codes for {city.name}, {state.name}"))

            self.stdout.write(self.style.SUCCESS('Data generation complete.'))
