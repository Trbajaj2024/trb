from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import (
    Carousel, Statistic, Program, Event, Testimonial, 
    Achievement, LiveClass, Course, Subject, Chapter, 
    VideoLecture
)
from datetime import timedelta
import os
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates all demo data for the website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting demo data population...')

        # Clear existing data
        self.clear_existing_data()

        # Populate all sections
        self.create_carousels()
        self.create_statistics()
        self.create_programs()
        self.create_events()
        self.create_achievements()
        self.create_live_classes()
        self.create_courses()

        self.stdout.write(self.style.SUCCESS('Successfully populated all demo data'))

    def clear_existing_data(self):
        Carousel.objects.all().delete()
        Statistic.objects.all().delete()
        Program.objects.all().delete()
        Event.objects.all().delete()
        Achievement.objects.all().delete()
        LiveClass.objects.all().delete()
        Course.objects.all().delete()

    def create_carousels(self):
        carousels_data = [
            {
                'title': 'Welcome to TRBSS',
                'subtitle': 'Empowering Minds, Shaping Futures',
                'image': 'carousel/school-main.jpg',
                'order': 1
            },
            {
                'title': 'Excellence in Education',
                'subtitle': 'State-of-the-art Facilities and Expert Faculty',
                'image': 'carousel/classroom.jpg',
                'order': 2
            },
            {
                'title': 'Holistic Development',
                'subtitle': 'Sports, Arts, and Academic Excellence',
                'image': 'carousel/sports.jpg',
                'order': 3
            }
        ]

        for data in carousels_data:
            Carousel.objects.create(**data)

    def create_statistics(self):
        stats_data = [
            {
                'name': 'Students',
                'value': '1000+',
                'icon': 'fas fa-user-graduate',
                'order': 1
            },
            {
                'name': 'Teachers',
                'value': '50+',
                'icon': 'fas fa-chalkboard-teacher',
                'order': 2
            },
            {
                'name': 'Success Rate',
                'value': '95%',
                'icon': 'fas fa-chart-line',
                'order': 3
            },
            {
                'name': 'Years of Excellence',
                'value': '25+',
                'icon': 'fas fa-award',
                'order': 4
            }
        ]

        for data in stats_data:
            Statistic.objects.create(**data)

    def create_programs(self):
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

        for data in programs_data:
            Program.objects.create(
                title=data['title'],
                description=data['description'],
                icon=data['icon'],
                order=data['order'],
                is_active=True
            )

    def create_events(self):
        events_data = [
            {
                'title': 'Annual Sports Day',
                'description': 'Join us for a day of athletic excellence and sportsmanship.',
                'date': timezone.now() + timedelta(days=15),
                'image': 'events/sports-day.jpg',
                'is_featured': True
            },
            {
                'title': 'Science Exhibition',
                'description': 'Showcase of innovative projects by our young scientists.',
                'date': timezone.now() + timedelta(days=30),
                'image': 'events/science-fair.jpg',
                'is_featured': True
            },
            {
                'title': 'Cultural Festival',
                'description': 'Celebration of art, music, and cultural diversity.',
                'date': timezone.now() + timedelta(days=45),
                'image': 'events/cultural-fest.jpg',
                'is_featured': True
            }
        ]

        for data in events_data:
            Event.objects.create(**data)

    def create_achievements(self):
        achievements_data = [
            {
                'title': 'Best School Award',
                'description': 'Recognized as the best school in the region',
                'date': timezone.now() - timedelta(days=30),
                'image': 'achievements/award.jpg',
                'is_featured': True
            },
            {
                'title': 'Sports Championship',
                'description': 'Won the inter-school sports championship',
                'date': timezone.now() - timedelta(days=60),
                'image': 'achievements/sports.jpg',
                'is_featured': True
            },
            {
                'title': 'Academic Excellence',
                'description': '100% success rate in board examinations',
                'date': timezone.now() - timedelta(days=90),
                'image': 'achievements/academic.jpg',
                'is_featured': True
            }
        ]

        for data in achievements_data:
            Achievement.objects.create(**data)

    def create_live_classes(self):
        live_classes_data = [
            {
                'title': 'Advanced Mathematics',
                'description': 'Live session on calculus and advanced algebra',
                'date': timezone.now() + timedelta(hours=2),
                'platform': 'Google Meet',
                'link': 'https://meet.google.com/xyz',
                'is_active': True
            },
            {
                'title': 'Physics Lab',
                'description': 'Virtual physics experiments and demonstrations',
                'date': timezone.now() + timedelta(hours=4),
                'platform': 'YouTube',
                'link': 'https://youtube.com/live/xyz',
                'is_active': True
            },
            {
                'title': 'English Literature',
                'description': 'Analysis of Shakespeare\'s works',
                'date': timezone.now() + timedelta(hours=6),
                'platform': 'Google Meet',
                'link': 'https://meet.google.com/abc',
                'is_active': True
            }
        ]

        for data in live_classes_data:
            LiveClass.objects.create(**data)

    def create_courses(self):
        courses_data = [
            {
                'title': 'Complete Python Programming',
                'description': 'Master Python programming from basics to advanced concepts.',
                'image': 'courses/python.jpg',
                'subjects': [
                    {
                        'title': 'Python Basics',
                        'chapters': [
                            {
                                'title': 'Introduction to Python',
                                'lectures': [
                                    {'title': 'What is Python?', 'video_id': 'Y8Tko2YC5hA', 'duration': '15:30'},
                                    {'title': 'Setting up Python', 'video_id': 'YYXdXT2l-Gg', 'duration': '12:45'},
                                ]
                            },
                        ]
                    }
                ]
            },
            # Add more courses as needed
        ]

        for course_data in courses_data:
            course = Course.objects.create(
                title=course_data['title'],
                description=course_data['description'],
                image=course_data['image'],
                is_active=True
            )
            
            for subject_data in course_data['subjects']:
                subject = Subject.objects.create(
                    course=course,
                    title=subject_data['title']
                )
                
                for chapter_data in subject_data['chapters']:
                    chapter = Chapter.objects.create(
                        subject=subject,
                        title=chapter_data['title']
                    )
                    
                    for lecture_data in chapter_data['lectures']:
                        VideoLecture.objects.create(
                            chapter=chapter,
                            title=lecture_data['title'],
                            video_id=lecture_data['video_id'],
                            duration=lecture_data['duration']
                        ) 