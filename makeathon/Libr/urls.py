from django.urls import path
from . import views

urlpatterns=[
path('home/',views.home,name='home'),
path('studentRegister/',views.studentRegister),
path('userRegister/',views.userRegister),
path('logging/',views.logging,name='Log_in'),
path('books/',views.list_books,name='all_books'),
path('bookissue/(?P<bookname>[0-9]+)/',views.issue_a_book,name='issue_it'),
path('bookreissue/(?P<booknum>[0-9]+)/',views.re_issue,name='reissue_it'),
path('logout/',views.logout_view,name='log_out'),
path('selectbooks/',views.select_books),
path('Contrib/',views.Contrib,name='con'),
path('addBooks/',views.Contrib,name='con'),
path('removebooks/(?P<booknum>[0-9]+)/',views.removebook,name='remove'),
path('allissues/',views.allissues,name='issue'),
path('about/',views.about,name='about'),
]
