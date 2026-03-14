import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.common.models import Farm, Role
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
  help = "Reset and seed farms + users with roles and active farm"

  def create_user(self, email):
    return User.objects.create_user(
      email=email,
      password=PASSWORD
    )

  @transaction.atomic
  def handle(self, *args, **kwargs):

    self.stdout.write("Removing old data...")

    Role.objects.all().delete()
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

    # SUPERUSER ADMIN
    admin_user = User.objects.create_superuser(
      email="admin@example.com",
      password=PASSWORD
    )
    Role.objects.create(
      user=admin_user,
      farm=farm1,
      role=UserRole.ADMIN,
      active=True
    )
    admin_user.active_farm = farm1
    admin_user.save()

    # FARM MANAGERS
    farm_manager = self.create_user("farm_manager@example.com")
    farm_manager2 = self.create_user("farm_manager2@example.com")

    # ENGINEERS
    eng1 = self.create_user("eng1@example.com")
    eng2 = self.create_user("eng2@example.com")
    eng3 = self.create_user("eng3@example.com")

    # EXECUTIVES
    exec1 = self.create_user("exec1@example.com")
    exec2 = self.create_user("exec2@example.com")
    exec3 = self.create_user("exec3@example.com")

    # LOGISTICS
    logistic1 = self.create_user("logistic1@example.com")
    logistic2 = self.create_user("logistic2@example.com")

    # AUDITORS
    auditor1 = self.create_user("auditor1@example.com")
    auditor2 = self.create_user("auditor2@example.com")

    # BUYERS
    buyer1 = self.create_user("buyer1@example.com")
    buyer2 = self.create_user("buyer2@example.com")

    self.stdout.write("Assigning roles to farms...")

    assignments = [
      # FARM MANAGERS
      (farm_manager, farm1, UserRole.FARMER),
      (farm_manager, farm2, UserRole.FARMER),
      (farm_manager2, farm1, UserRole.FARMER),

      # ENGINEERS
      (eng1, farm1, UserRole.ENGINEER),
      (eng2, farm1, UserRole.ENGINEER),
      (eng2, farm2, UserRole.ENGINEER),
      (eng3, farm2, UserRole.ENGINEER),

      # EXECUTIVES
      (exec1, farm1, UserRole.EXECUTIVE),
      (exec2, farm1, UserRole.EXECUTIVE),
      (exec3, farm1, UserRole.EXECUTIVE),

      # LOGISTICS
      (logistic1, farm1, UserRole.LOGISTIC),
      (logistic2, farm2, UserRole.LOGISTIC),

      # AUDITORS
      (auditor1, farm1, UserRole.AUDITOR),
      (auditor2, farm2, UserRole.AUDITOR),

      # BUYERS
      (buyer1, farm1, UserRole.BUYER),
      (buyer2, farm2, UserRole.BUYER),
    ]

    first_farm = {}
    for user, farm, role in assignments:
      Role.objects.create(
        user=user,
        farm=farm,
        role=role,
        active=True
      )
      if user not in first_farm:
        first_farm[user] = farm

    for user, farm in first_farm.items():
      if user != admin_user:
        user.active_farm = farm
        user.save()

    self.stdout.write(self.style.SUCCESS("Seeder completed successfully"))