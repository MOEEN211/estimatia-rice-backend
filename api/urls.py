from django.urls import path, include
from home.views import *

urlpatterns = [

    # Rice API views
    path('cr-rice/', create_rice),
    path('dt-rice/', detect_rice),
    path('rice/', get_rice),

    # Leaf API views
    path('creat-leaf/', create_leaf),
    path('leaves/', get_leaves),
    path('det-leaf/', detect_leaf)
]
