from django.urls import path

from analysis import views

urlpatterns = [
    path('', views.AssemblyView.as_view()),
    path('assembly/', views.AssemblyView.as_view()),
    path('assemblyPools/', views.AssemblyPoolsView.as_view()),
    path('analysis/', views.AnalysisView.as_view()),
]