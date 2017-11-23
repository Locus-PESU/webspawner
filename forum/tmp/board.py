from forum.models import Board, Category
import csv
import datetime
f = open('forum/tmp/board.csv', 'r')
reader = csv.reader(f)
next(reader)
for cat, name in reader:
    categ = Category.objects.get(pk=cat)
    Board.objects.create(category=categ, name=name,
                         created_on=datetime.datetime.now())
