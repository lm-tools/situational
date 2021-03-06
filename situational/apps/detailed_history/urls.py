from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'current_work$', views.CurrentWorkView.as_view(),
        name="current_work"),
    url(r'^$', views.StartView.as_view(),
        name="start"),
    url(r'work_change_1$', views.WorkChangeOneView.as_view(),
        name="work_change_1"),
    url(r'work_change_2$', views.WorkChangeTwoView.as_view(),
        name="work_change_2"),
    url(r'work_previous$', views.WorkPreviousView.as_view(),
        name="work_previous"),
    url(r'training_education$', views.TrainingEducationView.as_view(),
        name="training_education"),
    url(r'other_circumstances$', views.OtherCircumstancesView.as_view(),
        name="other_circumstances"),
    url(r'summary$', views.SummaryView.as_view(),
        name="summary"),
    url(r'send$', views.SendView.as_view(),
        name="send"),
    url(r'summary\.pdf$', views.PDFView.as_view(),
        name="pdf"),
    url(r'clear_session$', views.ClearSessionView.as_view(),
        name="clear_session"),
]
