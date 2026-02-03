from django.urls import path
from .views import UploadView, HistoryView, SummaryView, PDFView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('summary/<int:dataset_id>/', SummaryView.as_view(), name='summary'),
    path('pdf/<int:dataset_id>/', PDFView.as_view(), name='pdf'),
]
