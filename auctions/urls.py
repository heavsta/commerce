from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.categories_filter, name='categories_filter'),
    path('listings/create/', views.create_listing, name='create_listing'),
    path('listings/<int:listing_id>/', views.show_listing, name='show_listing'),
    path('listings/<int:listing_id>/close', views.close_auction, name='close_auction'),
    path('listings/<int:listing_id>/comment', views.post_comment, name='post_comment'),
    path('listings/<int:listing_id>/place_bid', views.place_bid, name='place_bid'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/add/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:listing_id>/', views.del_from_watchlist, name='del_from_watchlist'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register')
]
