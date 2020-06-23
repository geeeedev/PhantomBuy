from django.urls import path
from . import views

# NO Leading Slashes!!
# DIRECT GET and POST routes - GET will show route as URL path
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.success),
    path('logout', views.logout),
    path('sav/new', views.new),
    path('sav/create', views.create),
    path('sav/<id>/toggleComplete', views.toggleComplete),
    path('sav/<id>/toggleSave', views.toggleSave),
    path('sav/bulkUpdate', views.bulkUpdate),
    path('sav/<id>/edit', views.edit),
    path('sav/<id>/update', views.update),
    path('sav/<id>/delete', views.destroy),
    path('sav/deleteAll', views.destroyAll),
    path('items', views.displayItems),
    path('editItemPrice', views.editItemPrice),
    path('updateItemPrice', views.updateItemPrice),
]
