import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import User, Student

class Command(BaseCommand):
    help = 'Import students from CSV file'

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
                        is_student=True
                    )

                    # Create Student
                    Student.objects.create(
                        user=user,
                        roll_number=row['roll_number'],
                        grade=row['grade'],
                        section=row['section'],
                        parent_name=row['parent_name'],
                        parent_phone=row['parent_phone']
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created student: {user.username}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating student {row["username"]}: {str(e)}')
                    ) 