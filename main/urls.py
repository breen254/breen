from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('user_posts/', views.user_posts, name='user_posts'),
    # path('profile/', views.profile, name='profile'),
    path('about/', views.aboutPage, name='about'),    
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('create_post', views.create_post, name='create_post'),
    
    path('confirm_delete/<int:post_id>', views.confirm_delete, name='confirm_delete'),
    
    path('delete_post/<int:post_id>/delete', views.delete_post, name='delete_post'),
    
    path('add_to_favorites/<int:post_id>/', views.add_to_favorites, name='add_to_favorites'),
    
    path('post_detail/<int:post_id>', views.post_detail, name = 'post_detail'),
    path('increment_views/<int:post_id>/', views.increment_views, name='increment_views'), 
    
    path('view_user_posts/<int:user_id>/', views.view_user_posts, name='view_user_posts'),
    
    path('post/<int:pk>/', views.post_detailed, name='postdetail'),
    
    path('update_post/<int:pk>/', views.update_post, name='update_post'),

    
]
