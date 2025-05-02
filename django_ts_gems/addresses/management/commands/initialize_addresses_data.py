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
        with transaction.atomic():
            states = []
            for state_name in states_list:
                state, created = State.objects.get_or_create(name=state_name)
                if created:
                    states.append(state)

            self.stdout.write(self.style.SUCCESS(
                f"Created {len(states)} states."))

            for state in states:
                for _ in range(10):
                    city_name = fake.city()
                    city, created = City.objects.get_or_create(
                        name=city_name, state=state)
                    if created:
                        for _ in range(5):
                            zip_code = fake.zipcode()
                            zip_code_obj, created = ZipCode.objects.get_or_create(
                                code=zip_code, city=city)
                            if created:
                                for _ in range(5):
                                    street_address = fake.street_address()
                                    StreetAddress.objects.create(
                                        street_address=street_address,
                                        zip_code=zip_code_obj
                                    )

            self.stdout.write(self.style.SUCCESS('Data generation complete.'))
