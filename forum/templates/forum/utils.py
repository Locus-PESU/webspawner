from homeapp.models import SiteVisit, Quote
import datetime
from random import randint


def visit_count(f):
    def decorated_fn(*args, **kwargs):
        idt = 0
        request = args[0]
        if request.user.is_authenticated:
            idt = request.user.id
        params = {
            'referer': request.META.get('HTTP_REFERER'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }
        pr_time = datetime.datetime.today()
        SiteVisit.objects.create(identity=idt, time=pr_time, **params)
        quotes = Quote.objects.filter(displayed=False)
        if not quotes:
            quotes = Quote.objects.all()
            quotes.update(displayed=False)
        rand = randint(0, len(quotes))
        quote = quotes[rand]
        quote.displayed = True
        quote.save()
        context = {
            'quote': quote,
            'count': SiteVisit.objects.all().count(),
        }
        return f(context, *args, **kwargs)
    return decorated_fn


def trimmed_visit_count(f):
    def decorated_fn(*args, **kwargs):
        idt = 0
        request = args[0]
        if request.session.get('id', False):
            idt = request.session['id']
        else:
            request.session['id'] = SiteVisit.objects.distinct(
                'identity').count()
        params = {
            'referer': request.META.get('HTTP_REFERER'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }
        pr_time = datetime.datetime.today()
        SiteVisit.objects.create(identity=idt, time=pr_time, **params)
        context = {'count': SiteVisit.objects.all().count()}
        return f(context, *args, **kwargs)
    return decorated_fn
