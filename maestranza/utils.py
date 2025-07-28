from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import  get_object_or_404

def paginacion(request,modelo):
    paginator = Paginator(modelo, 10)
    page_number = request.GET.get('page',1)
    try:
        modelo = paginator.page(page_number)
    except EmptyPage:
        modelo = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        modelo = paginator.page(1)

    return modelo


def modo_gestion(modelo,id=None):
    if id:
        return get_object_or_404(modelo, id=id), 'editar', 0
    return None, 'crear', 1

