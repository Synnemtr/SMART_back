from django.contrib import admin
from django.urls import re_path, path, include
from django.conf import settings
from urllib.parse import urlparse
from django.conf.urls import url
from log_manager import views as log_manager_views
from .views import protected_serve, swagger_schema_view

admin.site.site_header = 'Sustain' + ' App v1'
admin.site.index_title = "Settings"
admin.site.site_url = '/log_manager/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_manager/', log_manager_views.table_log, name='log_manager'),
    path('api/v1/auth/', include('api.authentication.urls'), name='authentication'),
    path('api/v1/users/', include('api.user.urls'), name='user'),
    path('api/v1/achievements/', include('api.achievement.urls'), name='achievement'),
    path('api/v1/gamification-types/', include('api.gamification_type.urls'), name='gamification_type'),
    path('api/v1/badges/', include('api.badge.urls'), name='badge'),
    path('api/v1/gamification-questions/', include('api.gamification_question.urls'), name='gamification_question'),
    path('api/v1/gamification-profiles/', include('api.gamification_profile.urls'), name='gamification_profile'),
    path('api/v1/motivations/', include('api.motivation.urls'), name='motivation'),
    path('api/v1/motivation-questions/', include('api.motivation_question.urls'), name='motivation_question'),
    path('api/v1/motivation-profiles/', include('api.motivation_profile.urls'), name='motivation_profile'),
    path('api/v1/game-element/', include('api.game_element.urls'), name='game_element'),
    path('api/v1/game-element-quiz/', include('api.game_element_quiz.urls'), name='game_element_quiz'),
    path('api/v1/gamification-pointsystem/', include('api.gamification_pointsystem.urls'), name='gamification_pointsystem'),

    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            swagger_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', swagger_schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', swagger_schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc')
]

urlpatterns += [url(r'^%s(?P<path>.*)$' % urlparse(settings.MEDIA_URL).path[1:], protected_serve,
                     {'document_root': settings.MEDIA_ROOT})]
