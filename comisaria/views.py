from django.shortcuts import render, get_object_or_404, redirect
from .models import Comisaria
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ComisariaForm

# Create your views here.
