from comps.utils import today, get_all_items, update_db
from comps.models import Category, Sku
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        dt_check = Sku.objects.all().first()
        if not dt_check or dt_check.created_at.date() != today:
            cats = Category.objects.all()
            records = list()
            for cat in cats:
                records = get_all_items(cat)
                break
            last_sales = list()
            for rec in records:
                last_sales.append(rec['graph'][-1])
            if not any(last_sales):
                pass
            else:
                instance = Sku.objects.all()
                instance.delete()
                for cat in cats:
                    update_db(cat)
