# -*- coding: utf-8 -*-

from json import JSONEncoder
from datetime import datetime
import random
import string
from django.core import serializers
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from .models import User, Token, Expense, Income , News

# Create your views here.

# create random string for Toekn
random_str = lambda N: ''.join(
    random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# login , (API) , returns : JSON = statuns (ok|error) and token


@csrf_exempt
def news(request):
    news = News.objects.all().order_by('-date')[:11]
    news_serialized = serializers.serialize("json", news)
    return JsonResponse(news_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def login(request):
    # check if POST objects has username and password
    if request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            token = this_token.token
            context = {}
            context['result'] = 'ok'
            context['token'] = token
            # return {'status':'ok','token':'TOKEN'}
            return JsonResponse(context, encoder=JSONEncoder)
        else:
            context = {}
            context['result'] = 'error'
            # return {'status':'error'}
            return JsonResponse(context, encoder=JSONEncoder)
        
        
        
@csrf_exempt
@require_POST
def whoami(request):
    if request.POST.has_key('token'):
        this_token = request.POST['token']  # TODO: Check if there is no `token`- done-please Check it
        # Check if there is a user with this token; will retun 404 instead.
        this_user = get_object_or_404(User, token__token=this_token)

        return JsonResponse({
            'user': this_user.username,
        }, encoder=JSONEncoder)  # return {'user':'USERNAME'}

    else:
        return JsonResponse({
            'message': 'لطفا token را نیز ارسال کنید .',
        }, encoder=JSONEncoder)  #



@csrf_exempt
@require_POST
def query_expenses(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    expenses = Expense.objects.filter(user=this_user).order_by('-date')[:num]
    expenses_serialized = serializers.serialize("json", expenses)
    return JsonResponse(expenses_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def query_incomes(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    incomes = Income.objects.filter(user=this_user).order_by('-date')[:num]
    incomes_serialized = serializers.serialize("json", incomes)
    return JsonResponse(incomes_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 month
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    income = Income.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    expense = Expense.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    context = {}
    context['expense'] = expense
    context['income'] = income
    # return {'income':'INCOME','expanse':'EXPANSE'}
    return JsonResponse(context, encoder=JSONEncoder)


# homepage of System


def index(request):
    context = {}
    return render(request, 'index.html', context)



@csrf_exempt
@require_POST
def edit_expense(request):
    """edit an income"""
    print (request.POST)
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_pk = request.POST['id'] if 'id' in request.POST else "-1"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)
    
    this_expense = get_object_or_404(Expense, pk=this_pk, user=this_user)
    this_expense.text = this_text
    this_expense.amount = this_amount
    this_expense.save()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
@require_POST
def edit_income(request):
    """ edit an income """    
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_pk = request.POST['id'] if 'id' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    this_income = get_object_or_404(Income, pk=this_pk, user=this_user)
    this_income.text = this_text
    this_income.amount = this_amount
    this_income.save()

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

# submit an income to system (api) , input : token(POST) , output : status
# = (ok)


@csrf_exempt
@require_POST
def submit_income(request):
    """ submit an income """

    # TODO: revise validation for the amount
    this_date = request.POST['date'] if 'date' in request.POST else timezone.now()
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    Income.objects.create(user=this_user, amount=this_amount,
                          text=this_text, date=this_date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


# submit an expanse to system (api) , input : token(POST) , output :
# status = (ok)
@csrf_exempt
@require_POST
def submit_expense(request):
    """ submit an expense """

    # TODO: revise validation for the amount
    this_date = request.POST['date'] if 'date' in request.POST else timezone.now()
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    Expense.objects.create(user=this_user, amount=this_amount,
                           text=this_text, date=this_date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)  # return {'status':'ok'}

@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    redirect('/')