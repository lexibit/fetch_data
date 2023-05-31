"""
URL configuration for fetch_data project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from transaction.views import fetch_data #, calculate_balances
from transaction.views import TransactionListView
from transaction.views import login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('fetch-data/', fetch_data, name='fetch-data'),
    path('fetch-data/<str:chain>/<str:address>/', fetch_data, name='fetch_data'),
    # path('calculate-balances/', calculate_balances, name='calculate-balances'),
    path('api/transactions/', TransactionListView.as_view(), name='transaction-list'),

]
