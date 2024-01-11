from django.contrib import admin
from django.urls import path
from stripe_app.views import get_stripe_session_id, get_item_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:id>/', get_stripe_session_id),
    path('item/<int:id>/', get_item_page),
]
