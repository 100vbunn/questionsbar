from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.questions, name='questions'),
    path('registration', views.registration, name='registration'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('addanswer/<int:q_id>', views.add_answer, name='add_answer'),
    path('<int:q_id>', views.show_answer, name='show_answer'),
    path('question/<int:q_id>', views.show_question, name='show_question'),
    path('delete/<int:q_id>', views.delete_question, name='delete'),
    # path('<path:filename>', views.getfile, name='getfile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
