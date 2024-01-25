from django.urls import path
from . import views

urlpatterns = [
    path('' , views.submit_expense , name = 'submit_expense') ,
    path('' , views.submit_income , name = 'submit_income') ,

]
