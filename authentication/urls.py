from django.urls import path
from .views import LoginView, UserListView, UserRetrieveUpdateView, SignUpView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('users', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>', UserRetrieveUpdateView.as_view(), name='user-get-update-delete')
]