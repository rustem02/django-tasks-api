from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('tasks', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>', TaskRetrieveUpdateDestroyView.as_view(), name='task_rud'),
]
