from datetime import date, timedelta
from decimal import Decimal
import random

from django.core.management.base import BaseCommand

from accounts.models import User
from billing.models import Deduction
from collection.models import MilkEntry, RateChart
from farmers.models import CollectionCenter, Farmer


class Command(BaseCommand):
    help = 'Load demo users, farmers, rates, and sample milk entries'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@milkdairy.com', 'role': 'admin'},
        )
        if created:
            admin.set_password('admin123')
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()

        operator, created = User.objects.get_or_create(
            username='operator',
            defaults={'email': 'op@milk.com', 'role': 'operator'},
        )
        if created:
            operator.set_password('operator123')
            operator.save()

        accountant, created = User.objects.get_or_create(
            username='accountant',
            defaults={'email': 'acc@milk.com', 'role': 'accountant'},
        )
        if created:
            accountant.set_password('accountant123')
            accountant.save()

        center1, _ = CollectionCenter.objects.get_or_create(
            name='Main Center',
            defaults={'location': 'Village Road, Pune'},
        )
        center2, _ = CollectionCenter.objects.get_or_create(
            name='North Center',
            defaults={'location': 'North Block, Pune'},
        )

        rates = [
            ('Low Fat', Decimal('3.0'), Decimal('4.5'), Decimal('38.00')),
            ('Standard', Decimal('4.6'), Decimal('6.0'), Decimal('42.00')),
            ('High Fat', Decimal('6.1'), Decimal('10.0'), Decimal('48.00')),
        ]
        for name, min_f, max_f, price in rates:
            RateChart.objects.get_or_create(
                name=name,
                defaults={
                    'min_fat': min_f,
                    'max_fat': max_f,
                    'price_per_liter': price,
                },
            )

        farmers_data = [
            ('F001', 'Ramesh Patil', '9876500001', 'Wagholi', center1),
            ('F002', 'Suresh Jadhav', '9876500002', 'Hadapsar', center1),
            ('F003', 'Ganesh More', '9876500003', 'Kharadi', center2),
            ('F004', 'Vijay Kulkarni', '9876500004', 'Wagholi', center2),
            ('F005', 'Anil Deshmukh', '9876500005', 'Hadapsar', center1),
        ]

        farmer_user, created = User.objects.get_or_create(
            username='farmer1',
            defaults={'email': 'f1@milk.com', 'role': 'farmer'},
        )
        if created:
            farmer_user.set_password('farmer123')
            farmer_user.save()

        for i, (fid, name, phone, village, center) in enumerate(farmers_data):
            farmer, _ = Farmer.objects.get_or_create(
                farmer_id=fid,
                defaults={
                    'name': name,
                    'phone': phone,
                    'village': village,
                    'center': center,
                    'bank_account': f'123456789{i}',
                    'ifsc_code': 'SBIN0001234',
                    'animal_count': random.randint(2, 6),
                },
            )
            if i == 0:
                farmer.user = farmer_user
                farmer.save()

        shifts = ['morning', 'evening']
        today = date.today()
        for day_offset in range(-1, 11):
            entry_date = today - timedelta(days=day_offset)
            for farmer in Farmer.objects.all():
                if random.random() > 0.15:
                    shift = random.choice(shifts)
                    fat = Decimal(str(round(random.uniform(4.0, 7.5), 2)))
                    qty = Decimal(str(round(random.uniform(5, 25), 2)))
                    rate = RateChart.get_rate_for_fat(fat)
                    MilkEntry.objects.get_or_create(
                        farmer=farmer,
                        date=entry_date,
                        shift=shift,
                        defaults={
                            'quantity_liters': qty,
                            'fat_percent': fat,
                            'snf_percent': Decimal('8.5'),
                            'rate_per_liter': rate,
                            'total_amount': qty * rate,
                            'entered_by': operator,
                        },
                    )

        Deduction.objects.get_or_create(
            farmer=Farmer.objects.get(farmer_id='F001'),
            deduction_type='feed',
            month=today.replace(day=1),
            defaults={'amount': Decimal('500.00'), 'description': 'Cattle feed advance'},
        )

        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        self.stdout.write('Login: admin/admin123 | operator/operator123 | accountant/accountant123 | farmer1/farmer123')
