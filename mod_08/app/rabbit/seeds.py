import random
from datetime import date
from faker import Faker

import connect
from models import Customer


USER_NUMBER = 100


def main():
    fd = Faker('uk_UA')

    for _ in range(USER_NUMBER):
        Customer(
            fullname=fd.name(),
            email=fd.ascii_safe_email(),
            phone=fd.phone_number(),
            born_date=fd.date_between(
                start_date=date(1950, 1, 1),
                end_date=date(2005, 1, 1)
            ),
            address=fd.address(),
            notification_method=random.choice(['email', 'sms'])
        ).save()


if __name__ == "__main__":
    main()
