from django.urls import path
from . import views
from .views import UserLoginView
urlpatterns = [
    path('', views.registerUsers, name='register'),
    path('show/', views.showRegisteredUser, name='show'),
    path('send/', views.getDataFromUser, name='send'),
    path('update/<int:id>', views.updateUser, name='update'),
    path('delete/<int:id>', views.deleteUser, name='delete'),
    # Login Routes
    path('create/', UserLoginView.userCreate, name='createuser'),
    path('login/', UserLoginView.userLogin, name='login'),
    path('home/', UserLoginView.userHome, name='home'),
    path('logout/', UserLoginView.userLogout, name='logout'),
]