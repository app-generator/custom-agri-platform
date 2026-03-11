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
        user = User.objects.create_user(
            email=email,
            password=PASSWORD,
            role=role
        )
        return user

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Removing old data...")

        FarmMembership.objects.all().delete()
        Farm.objects.all().delete()

        User.objects.filter(email__in=[
            "farm_manager@example.com",
            "farm_manager2@example.com",
            "eng1@example.com",
            "eng2@example.com",
            "eng3@example.com",
            "exec1@example.com",
            "exec2@example.com",
            "exec3@example.com",
        ]).delete()

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

        farm_manager = self.create_user(
            "farm_manager@example.com",
            UserRole.FARMER
        )

        farm_manager2 = self.create_user(
            "farm_manager2@example.com",
            UserRole.FARMER
        )

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

        self.stdout.write("Assigning farms...")

        assignments = [
            (farm_manager, farm1),
            (farm_manager, farm2),

            (farm_manager2, farm1),

            (eng1, farm1),

            (eng2, farm1),
            (eng2, farm2),

            (eng3, farm2),

            (exec1, farm1),
            (exec2, farm1),
            (exec3, farm1),
        ]

        for user, farm in assignments:
            FarmMembership.objects.create(
                user=user,
                farm=farm
            )

        self.stdout.write(self.style.SUCCESS("Seeder completed successfully"))