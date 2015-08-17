from django.conf.urls import patterns, url

from history import views

urlpatterns = patterns(
    '',
    # url(r'details', views.HistoryDetailsView.as_view(), name="details"),
    # url(r'report', views.HistoryReportView.as_view(), name="report"),
    url(r'clear_session', views.ClearSessionView.as_view(),
        name="clear_session"),
    url(r'current_work', views.CurrentWorkView.as_view(),
        name="current_work"),
    url(r'start_text', views.HistoryStartView.as_view(),
        name="start_text"),
    url(r'start_structured', views.HistoryStartStructuredView.as_view(),
        name="start_structured"),
    url(r'work_change_1', views.WorkChangeOneView.as_view(),
        name="work_change_1"),
    url(r'work_change_2', views.WorkChangeTwoView.as_view(),
        name="work_change_2"),
    url(r'work_previous', views.WorkPreviousView.as_view(),
        name="work_previous"),
    url(r'training_education', views.TrainingEducationView.as_view(),
        name="training_education"),
    url(r'other_circumstances', views.OtherCircumstancesView.as_view(),
        name="other_circumstances"),
    url(r'summary', views.SummaryView.as_view(),
        name="summary")
)
