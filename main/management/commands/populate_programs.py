from django.core.management.base import BaseCommand
from main.models import Program

class Command(BaseCommand):
    help = 'Populates demo data for Featured Programs'

    def handle(self, *args, **kwargs):
        programs_data = [
            {
                'title': 'Science & Technology',
                'description': 'Explore cutting-edge STEM education with hands-on experiments, robotics, and innovative learning methods. Our science program nurtures future innovators and problem-solvers.',
                'icon': 'fas fa-microscope',
                'order': 1,
            },
            {
                'title': 'Arts & Creativity',
                'description': 'Discover your creative potential through visual arts, music, drama, and digital media. Our arts program develops imagination and self-expression.',
                'icon': 'fas fa-palette',
                'order': 2,
            },
            {
                'title': 'Sports Excellence',
                'description': 'Build strength, teamwork, and leadership through our comprehensive sports program. Features state-of-the-art facilities and professional coaching.',
                'icon': 'fas fa-running',
                'order': 3,
            },
            {
                'title': 'Language & Literature',
                'description': 'Master multiple languages and develop strong communication skills. Our program includes creative writing, public speaking, and cultural studies.',
                'icon': 'fas fa-book-reader',
                'order': 4,
            },
            {
                'title': 'Digital Innovation',
                'description': 'Learn coding, web development, and digital design. Prepare for the future with our cutting-edge technology curriculum.',
                'icon': 'fas fa-laptop-code',
                'order': 5,
            },
            {
                'title': 'Leadership Development',
                "description": "Develop essential leadership skills through workshops, community service, and real-world projects. Shape tomorrow's leaders today.",
                'icon': 'fas fa-users',
                'order': 6,
            }
        ]

        # Clear existing programs
        Program.objects.all().delete()

        # Create new programs
        for program_data in programs_data:
            Program.objects.create(
                title=program_data['title'],
                description=program_data['description'],
                icon=program_data['icon'],
                order=program_data['order'],
                is_active=True
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated featured programs'))