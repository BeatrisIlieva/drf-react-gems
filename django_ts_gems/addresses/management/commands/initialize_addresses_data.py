import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from django_ts_gems.addresses.models.state import State
from django_ts_gems.addresses.models.city import City
from django_ts_gems.addresses.models.zip_code import ZipCode
from django_ts_gems.addresses.models.street_address import StreetAddress

fake = Faker()

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
