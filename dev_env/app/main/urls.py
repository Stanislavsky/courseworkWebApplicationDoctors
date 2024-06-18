from django.urls import path
from main import views 

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('login/registration/', views.registration, name='registration'),
    path('electronic-medical-card/', views.electronic_medical_card, name='electronic_medical_card'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('save_changes/', views.save_changes, name='save_changes'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)