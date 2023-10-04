from django.urls import path
from .views import MyOrganizationsCompanyListView, AllCompanyListView, CreateCompanyView, EditCompanyView, DeleteCompanyView, CompanyDetailView

urlpatterns = [
    # display all companies owned by the user
    path('my-organizations/', MyOrganizationsCompanyListView.as_view(), name='my_organizations'),

    # list all companies
    path('', AllCompanyListView.as_view(), name='list_companies'),

    # create company
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    
    # edit company
    path('<int:pk>/edit/', EditCompanyView.as_view(), name='edit_company'),

    # delete company
    path('<int:pk>/delete/', DeleteCompanyView.as_view(), name='delete_company'),

    # company detail
    path('<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),

]