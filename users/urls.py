from django.contrib import admin
from django.urls import path
from users import views as user_view



urlpatterns = [
    path('users',user_view.UserDetailListView.as_view()),
    path('create-permission-for-role/', user_view.CreatePermissionForRoleView.as_view(), name='create-permission-for-role'),
    path('assign-permission-to-role/', user_view.AssignPermissionToRoleView.as_view(), name='assign-permission-to-role'),
    path('someview',user_view.SomeView.as_view()),
]