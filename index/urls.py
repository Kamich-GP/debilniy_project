from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page),
    path('category/<int:pk>', views.category_page),
    path('product/<int:pk>', views.product_page),
    path('register', views.Register.as_view()),
    path('reg-end', views.reg_end),
    path('logout', views.logout_view),
    path('search', views.search)
]
