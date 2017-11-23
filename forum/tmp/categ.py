from forum.models import Category, Board
import csv
import datetime
f = open('forum/tmp/category.csv', 'r')
reader = csv.reader(f)
next(reader)
for cat in reader:
    Category.objects.create(name=cat[0], created_on=datetime.datetime.now())
