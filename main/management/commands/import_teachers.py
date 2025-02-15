import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import User, Teacher

class Command(BaseCommand):
    help = 'Import teachers from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Create User
                    user = User.objects.create(
                        username=row['username'],
                        email=row['email'],
                        password=make_password(row['password']),
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone=row['phone'],
                        address=row['address'],
                        is_teacher=True
                    )

                    # Create Teacher
                    Teacher.objects.create(
                        user=user,
                        employee_id=row['employee_id'],
                        subject=row['subject'],
                        qualification=row['qualification']
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created teacher: {user.username}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating teacher {row["username"]}: {str(e)}')
                    ) 