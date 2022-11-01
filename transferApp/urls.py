# myapi/urls.py
from django.urls import include, path
from . import views
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('history/', views.HistoryView.as_view(),name='history'),
    path('users/',views.UsersView.as_view(),name='list_users'),
    path('profile/',views.ProfileView.as_view(),name='profile_details'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
