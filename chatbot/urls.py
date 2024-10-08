

# from django.urls import path
# from .views import index

# urlpatterns = [
#     path('', index, name='index'),
# ]
from django.urls import path
from .views import pdf_qa_view

urlpatterns = [
    path('', pdf_qa_view, name='pdf_qa_view'),
]
