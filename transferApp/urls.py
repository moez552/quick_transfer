# myapi/urls.py
from django.urls import include, path
from . import views
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('history/', views.HistoryView.as_view()),
    path('users/',views.UsersView.as_view()),
    path('profile/',views.ProfileView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]