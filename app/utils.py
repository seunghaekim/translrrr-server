from django.core.paginator import Paginator

def paginator_serializer(items, page, **kwargs):
    items_per_page = 1
    if 'per_page' in kwargs:
        items_per_page = kwargs['per_page']

    pages = Paginator(items, items_per_page)
    items = pages.page(page)

    result = {}
    result['total'] = pages.count
    result['num_pages'] = pages.num_pages
    result['items'] = items.object_list
    result['page'] = page
    result['has_next'] = items.has_next()
    result['has_previous'] = items.has_previous()
    result['has_other_pages'] = items.has_other_pages()

    return result


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def safe_request_get(request, key, default=None):
    if key in request.GET:
        return request.GET[key]
    return default


def safe_request_post(request, key, default=None):
    if key in request.POST:
        return request.POST[key]
    return default


def key_exsits_or_default(d, key, default=None):
    if key in d:
        return d[key]
    return default
