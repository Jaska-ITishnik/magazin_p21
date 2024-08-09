from datetime import datetime

from django.template import Library

register = Library()

@register.filter()
def is_new(created_at: datetime):
    now = datetime.now()
    return now.day - created_at.day <= 7 and now.month == created_at.month and \
           now.year == created_at.year


@register.filter()
def tittle_part(review: str):
    return review.split()[:5]