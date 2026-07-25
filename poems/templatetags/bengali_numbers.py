from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='bengali_num')
def to_bengali_number(value):
    """Convert English numbers to Bengali numerals"""
    if value is None:
        return '০'
    
    bengali_digits = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }
    
    value_str = str(value)
    result = ''
    for char in value_str:
        result += bengali_digits.get(char, char)
    
    return result


@register.filter(name='bengali_date')
def to_bengali_date(value):
    """Convert date to Bengali format"""
    if not value:
        return ''
    
    # Bengali month names
    bengali_months = {
        1: 'জানুয়ারী', 2: 'ফেব্রুয়ারী', 3: 'মার্চ',
        4: 'এপ্রিল', 5: 'মে', 6: 'জুন',
        7: 'জুলাই', 8: 'আগস্ট', 9: 'সেপ্টেম্বর',
        10: 'অক্টোবর', 11: 'নভেম্বর', 12: 'ডিসেম্বর'
    }
    
    # Bengali weekdays
    bengali_weekdays = {
        0: 'সোমবার', 1: 'মঙ্গলবার', 2: 'বুধবার',
        3: 'বৃহস্পতিবার', 4: 'শুক্রবার', 5: 'শনিবার', 6: 'রবিবার'
    }
    
    day = value.day
    month = value.month
    year = value.year
    
    # Convert day and year to Bengali numerals
    day_bn = to_bengali_number(day)
    year_bn = to_bengali_number(year)
    
    return f'{day_bn} {bengali_months[month]}, {year_bn}'