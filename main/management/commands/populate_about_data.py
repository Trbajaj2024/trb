from django.core.management.base import BaseCommand
from main.models import AboutPage, Feature, TimelineEvent, CoreValue, CallToAction

class Command(BaseCommand):
    help = 'Populates initial data for the About page'

    def handle(self, *args, **kwargs):
        # Create About Page content
        AboutPage.objects.get_or_create(
            hero_title="About TRBSS",
            hero_subtitle="Nurturing Minds, Building Futures Since 1995",
            welcome_title="Welcome to Excellence",
            welcome_description="At TRBSS, we believe in providing world-class education that nurtures both academic excellence and character development."
        )

        # Create Features
        features_data = [
            {
                'title': 'Academic Excellence',
                'description': 'Consistently achieving outstanding results',
                'icon': 'fas fa-graduation-cap',
                'order': 1
            },
            {
                'title': 'Holistic Development',
                'description': 'Focus on character and skills development',
                'icon': 'fas fa-users',
                'order': 2
            }
        ]

        for data in features_data:
            Feature.objects.get_or_create(**data)

        # Create Timeline Events
        timeline_data = [
            {
                'year': '1995',
                'title': 'Foundation',
                'description': 'Founded with a vision to provide quality education',
                'order': 1
            },
            {
                'year': '2005',
                'title': 'Expansion',
                'description': 'Expanded facilities and introduced new programs',
                'order': 2
            },
            {
                'year': '2015',
                'title': 'Excellence',
                'description': 'Achieved excellence in academic and extra-curricular activities',
                'order': 3
            },
            {
                'year': '2023',
                'title': 'Innovation',
                'description': 'Continuing to innovate and excel in modern education',
                'order': 4
            }
        ]

        for data in timeline_data:
            TimelineEvent.objects.get_or_create(**data)

        # Create Call to Actions
        cta_data = [
            {
                'title': 'Join Our School Community',
                'subtitle': 'Take the first step towards excellence in education',
                'button_text': 'Apply Now',
                'button_link': '/admissions/',
                'location': 'about_page'
            }
        ]

        for data in cta_data:
            CallToAction.objects.get_or_create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully populated About page data')) 