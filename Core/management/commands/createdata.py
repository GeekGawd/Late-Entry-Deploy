from random import randint, choice
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from faker import Faker
from Core.models import *
import faker.providers


class Command(BaseCommand):
    help = 'Command Information'

    def handle(self, *args, **kwargs):
        fake = Faker(["en_IN"])

        for _ in range(200000, 300000):
            st_no = _
            name = "Test"
            branch = Branch.objects.get(name="IT")
            batch = Batch.objects.get(batch=2019)

            Student.objects.create(
                student_no = st_no,
                name = name,
                branch = branch,
                batch = batch
            )
