from django.urls import path
from . import views

urlpatterns = [
    path(r'submit/expense/', views.submit_expense, name='submit_expense'),
    path(r'edit/expense/', views.edit_expense, name='edit_expense'),
    path(r'submit/income/', views.submit_income, name='submit_income'),
    path(r'edit/income/', views.edit_income, name='edit_income'),
    path(r'q/generalstat/', views.generalstat, name='generalstat'),
    path(r'q/incomes/', views.query_incomes, name='query_incomes'),
    path(r'q/expenses/', views.query_expenses, name='query_expenses'),
    path(r'accounts/whoami/', views.whoami, name='whoami'),
    path(r'accounts/login/', views.login, name='login'),
    path(r'news/', views.news, name='news'),
    path(r'', views.index, name='index'),
]
