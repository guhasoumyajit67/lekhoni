from django.core.management.base import BaseCommand
from poems.models import Category


class Command(BaseCommand):
    help = 'Create initial categories for Lekhoni'

    def handle(self, *args, **options):
        categories = [
            ('প্রেম', 'love', 'প্রেমের কবিতা', 'fa-heart'),
            ('বিষাদ', 'sad', 'বিষাদময় কবিতা', 'fa-sad-tear'),
            ('আনন্দ', 'happy', 'আনন্দের কবিতা', 'fa-smile'),
            ('একাকিত্ব', 'lonely', 'একাকিত্বের কবিতা', 'fa-user'),
            ('আশা', 'hope', 'আশার কবিতা', 'fa-sun'),
            ('প্রকৃতি', 'nature', 'প্রকৃতির কবিতা', 'fa-tree'),
            ('বর্ষা', 'rain', 'বর্ষার কবিতা', 'fa-cloud-rain'),
            ('বসন্ত', 'spring', 'বসন্তের কবিতা', 'fa-seedling'),
            ('শরৎ', 'autumn', 'শরতের কবিতা', 'fa-leaf'),
            ('দেশপ্রেম', 'patriotism', 'দেশপ্রেমের কবিতা', 'fa-flag'),
            ('মুক্তিযুদ্ধ', 'liberation_war', 'মুক্তিযুদ্ধের কবিতা', 'fa-fist-raised'),
            ('জীবন', 'life', 'জীবনের কবিতা', 'fa-life-ring'),
            ('স্বপ্ন', 'dream', 'স্বপ্নের কবিতা', 'fa-moon'),
            ('সংগ্রাম', 'struggle', 'সংগ্রামের কবিতা', 'fa-hand-fist'),
            ('যাত্রা', 'journey', 'যাত্রার কবিতা', 'fa-road'),
            ('আধ্যাত্মিক', 'spiritual', 'আধ্যাত্মিক কবিতা', 'fa-spa'),
            ('আধুনিক', 'modern', 'আধুনিক কবিতা', 'fa-laptop'),
            ('নারীবাদ', 'feminism', 'নারীবাদী কবিতা', 'fa-venus'),
            ('প্রতিবাদ', 'protest', 'প্রতিবাদী কবিতা', 'fa-bullhorn'),
            ('শিশুতোষ', 'children', 'শিশুতোষ কবিতা', 'fa-child'),
            ('রসাত্মক', 'humor', 'রসাত্মক কবিতা', 'fa-laugh'),
            ('অন্যান্য', 'other', 'অন্যান্য কবিতা', 'fa-ellipsis-h'),
        ]

        created_count = 0
        for name, slug, description, icon in categories:
            obj, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': description,
                    'icon': icon
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⏭️ Already exists: {name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Created {created_count} new categories!'
        ))