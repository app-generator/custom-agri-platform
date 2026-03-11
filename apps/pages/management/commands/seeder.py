import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.common.models import Farm, FarmMembership
from apps.users.models import UserRole

User = get_user_model()

PASSWORD = "Pass12__"

def random_romania_address():
    cities = [
        "Bucharest", "Cluj-Napoca", "Timișoara",
        "Iași", "Constanța", "Brașov", "Sibiu"
    ]

    streets = [
        "Strada Libertății",
        "Strada Unirii",
        "Strada Republicii",
        "Strada Victoriei",
        "Strada Mihai Eminescu"
    ]

    return f"{random.choice(streets)} {random.randint(1,120)}, {random.choice(cities)}, Romania"


class Command(BaseCommand):
    help = "Reset and seed farms + users"

    def create_user(self, email, role):
        return User.objects.create_user(
            email=email,
            password=PASSWORD,
            role=role
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Removing old data...")

        FarmMembership.objects.all().delete()
        Farm.objects.all().delete()

        User.objects.all().delete()

        self.stdout.write("Creating farms...")

        farm1 = Farm.objects.create(
            name="farm1",
            address=random_romania_address()
        )

        farm2 = Farm.objects.create(
            name="farm2",
            address=random_romania_address()
        )

        self.stdout.write("Creating users...")

        # FARM MANAGERS
        farm_manager = self.create_user(
            "farm_manager@example.com",
            UserRole.FARMER
        )

        farm_manager2 = self.create_user(
            "farm_manager2@example.com",
            UserRole.FARMER
        )

        # ENGINEERS
        eng1 = self.create_user(
            "eng1@example.com",
            UserRole.ENGINEER
        )

        eng2 = self.create_user(
            "eng2@example.com",
            UserRole.ENGINEER
        )

        eng3 = self.create_user(
            "eng3@example.com",
            UserRole.ENGINEER
        )

        # EXECUTIVES
        exec1 = self.create_user(
            "exec1@example.com",
            UserRole.EXECUTIVE
        )

        exec2 = self.create_user(
            "exec2@example.com",
            UserRole.EXECUTIVE
        )

        exec3 = self.create_user(
            "exec3@example.com",
            UserRole.EXECUTIVE
        )

        # LOGISTICS
        logistic1 = self.create_user(
            "logistic1@example.com",
            UserRole.LOGISTIC
        )

        logistic2 = self.create_user(
            "logistic2@example.com",
            UserRole.LOGISTIC
        )

        # AUDITORS
        auditor1 = self.create_user(
            "auditor1@example.com",
            UserRole.AUDITOR
        )

        auditor2 = self.create_user(
            "auditor2@example.com",
            UserRole.AUDITOR
        )

        # BUYERS
        buyer1 = self.create_user(
            "buyer1@example.com",
            UserRole.BUYER
        )

        buyer2 = self.create_user(
            "buyer2@example.com",
            UserRole.BUYER
        )

        self.stdout.write("Assigning farms...")

        assignments = [
            # FARM MANAGERS
            (farm_manager, farm1),
            (farm_manager, farm2),
            (farm_manager2, farm1),

            # ENGINEERS
            (eng1, farm1),
            (eng2, farm1),
            (eng2, farm2),
            (eng3, farm2),

            # EXECUTIVES
            (exec1, farm1),
            (exec2, farm1),
            (exec3, farm1),

            # LOGISTICS
            (logistic1, farm1),
            (logistic2, farm2),

            # AUDITORS
            (auditor1, farm1),
            (auditor2, farm2),

            # BUYERS
            (buyer1, farm1),
            (buyer2, farm2),
        ]

        for user, farm in assignments:
            FarmMembership.objects.create(
                user=user,
                farm=farm
            )

        self.stdout.write(self.style.SUCCESS("Seeder completed successfully"))