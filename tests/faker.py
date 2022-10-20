from faker import Faker
from faker.providers import lorem, date_time, person

faker = Faker()
faker.add_provider(lorem)
faker.add_provider(date_time)
faker.add_provider(person)
