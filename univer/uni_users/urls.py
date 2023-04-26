from django.urls import path
from .views import OrganizationRegistrationList, OrganizationRegistrationDetail
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('organizations/', login_required(OrganizationRegistrationList.as_view()), name='organization-list'),
    path('organizations/<int:pk>/', login_required(OrganizationRegistrationDetail.as_view()), name='organization-detail'),
]
