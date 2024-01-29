from django.urls import path
from . import views

app_name='topfragmarket'

urlpatterns = [
   path('', views.index, name='home'),
   path('about/', views.about, name='about'),
   path('categories/', views.categories, name='categories'), 
   path('accounts/login/', views.login_user, name='login'), 
      path('accounts/register/', views.register_user, name='register'),
   path('logout/', views.logout_user, name='logout'), 
   path('dashboard/', views.dashboard, name='dashboard'),
   path('profile/create/', views.create_profile, name="create_profile"),
   path('profile/<int:user_id>/', views.profile, name='profile'),
   path('listings/', views.listings, name='listings'),
      path('listings/<int:listing_id>', views.listing_detail, name='listing_detail'),
      path('listings/create/', views.create_listing, name='create_listing'),
      path('listings/<int:listing_id>/update-status/', views.update_listing_status, name='update_listing_status'),
      path('listings/<int:listing_id>/update/', views.update_listing, name='update_listing'),
      path('listings/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
   path('chats/', views.chats, name="chats"),
      path('chats/<int:chat_id>', views.chat_detail, name='chat_detail'),
   path('forum/', views.forum, name='forum'),
      path('forum/threads/<int:thread_id>', views.thread_detail, name='thread_detail'),
      path('forum/threads/create/', views.create_thread, name='create_thread'),
      path('forum/threads/<int:thread_id>/update', views.update_thread, name='update_thread'),
      path('forum/threads/<int:thread_id>/delete', views.delete_thread, name='delete_thread'),
]