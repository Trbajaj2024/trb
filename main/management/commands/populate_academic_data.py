from django.core.management.base import BaseCommand
from main.models import AcademicLevel, Department, Curriculum
from django.core.files import File
from django.conf import settings
import os
from pathlib import Path
from PIL import Image

class Command(BaseCommand):
    help = 'Populates initial academic data'

    def handle(self, *args, **kwargs):
        # Ensure media directories exist
        media_root = Path(settings.MEDIA_ROOT)
        dept_images_dir = media_root / 'departments'
        dept_images_dir.mkdir(parents=True, exist_ok=True)

        # Create Academic Levels
        levels_data = [
            {
                'name': 'Primary School',
                'description': 'Foundation years focusing on core skills and creative development',
                'icon': 'fas fa-child',
                'order': 1
            },
            {
                'name': 'Secondary School',
                'description': 'Comprehensive education with diverse subject choices',
                'icon': 'fas fa-school',
                'order': 2
            },
            {
                'name': 'Higher Secondary',
                'description': 'Specialized streams preparing for higher education',
                'icon': 'fas fa-graduation-cap',
                'order': 3
            }
        ]

        for data in levels_data:
            level, created = AcademicLevel.objects.get_or_create(
                name=data['name'],
                defaults=data
            )

            if created:
                # Create curriculum for this level
                Curriculum.objects.create(
                    title=f"{data['name']} Curriculum",
                    description=f"Comprehensive curriculum for {data['name']}",
                    academic_level=level,
                    subjects="Mathematics\nScience\nEnglish\nSocial Studies\nComputer Science"
                )

        # Create Departments with default images
        departments_data = [
            {
                'name': 'Science Department',
                'description': 'Cutting-edge science education with modern laboratories',
                'head_name': 'Dr. John Smith',
                'head_qualification': 'Ph.D. in Physics',
                'order': 1,
                'default_image': 'science-dept.jpg'
            },
            {
                'name': 'Mathematics Department',
                'description': 'Excellence in mathematical education and problem-solving',
                'head_name': 'Prof. Sarah Johnson',
                'head_qualification': 'M.Sc. in Mathematics',
                'order': 2,
                'default_image': 'math-dept.jpg'
            },
            {
                'name': 'Languages Department',
                'description': 'Comprehensive language education in multiple languages',
                'head_name': 'Dr. Maria Garcia',
                'head_qualification': 'Ph.D. in Literature',
                'order': 3,
                'default_image': 'lang-dept.jpg'
            }
        ]

        # Create placeholder images if they don't exist
        placeholder_path = media_root / 'departments' / 'placeholder.jpg'
        if not placeholder_path.exists():
            # Create a simple colored rectangle as placeholder
            img = Image.new('RGB', (800, 600), color='#0d6efd')
            img.save(placeholder_path)

        for data in departments_data:
            default_image = data.pop('default_image')
            dept, created = Department.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            
            if created or not dept.image:
                # Use placeholder image
                with open(placeholder_path, 'rb') as img_file:
                    dept.image.save(
                        default_image,
                        File(img_file),
                        save=True
                    )

        self.stdout.write(self.style.SUCCESS('Successfully populated academic data')) 