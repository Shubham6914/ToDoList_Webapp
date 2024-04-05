from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,UserLoginView,LogoutView,RegistratioinPage
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(),name='task'),  # this is stastic view 
    path('task_create/',TaskCreate.as_view(),name='task_create'), # this is also stastic view 
    path('login/',UserLoginView.as_view(),name='login'), # this is also stastic view 
    path('register/', RegistratioinPage.as_view(),name="register"),
    path('logout/',LogoutView,name='logout'), # this is also stastic view 
    path('task/<int:pk>/', TaskDetail.as_view(),name='task_details'), # this is dynamic view 
    path('task_update/<int:pk>/', TaskUpdate.as_view(),name='task_update'),# this is also dynamic view
    path('task_delete/<int:pk>/', TaskDelete.as_view(),name='task_delete'),# this is also dynamic view
     
    
]
