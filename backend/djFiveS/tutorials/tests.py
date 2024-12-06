from django.test import TestCase
from tutorials.models import models
from tutorials.models import stock_list

# Create your tests here.

query = stock_list.objects.all()
print(query)

s = stock_list(id = '23').save()
