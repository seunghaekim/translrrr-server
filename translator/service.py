# check hash in contentshash exists
# if hash in contentshash exists is false:
#   create hash to contentshash
#   create contents cach
# elif true:
#   get data from contentscache
#   if data creatime is expired:
#       request translate
#       update contents cache
#   else:
#       return data

from translator.models import ContentsHash
from translator.models import ContentsCache
from datetime import timedelta
from app.dbutils import datetimenow
from translator import exceptions

CACHE_EXPIRED_TIMEDELTA = {'days': 30}


def get_contents_hash_obj(contents_hash):
    try:
        contentshash_obj = ContentsHash.objects.get(contents_hash=contents_hash)
    except ContentsHash.DoesNotExist:
        return False
    return contentshash_obj


def create_contents_hash(contents_hash):
    contentshash = ContentsHash()
    contentshash.contents_hash = contents_hash
    contentshash.save()
    return contentshash


def get_contents_cache_obj(**kwargs):
    """[summary]

    Arguments:
        **kwargs
            contentshash_obj {[type]} -- [description]
            vendor {[type]} -- [description]
            source {[type]} -- [description]
            target {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    filter_kwargs = {
        'contents_hash': kwargs['contentshash_obj'],
        'vendor': kwargs['vendor'],
        'source': kwargs['source'],
        'target': kwargs['target'],
    }

    try:
        contentscache = ContentsCache.objects.filter(**filter_kwargs).get()
    except ContentsCache.DoesNotExist:
        return False
    return contentscache


def get_contents_cache(**kwargs):
    """[summary]

    Arguments:
        **kwargs
            contentshash_obj {[type]} -- [description]
            vendor {[type]} -- [description]
            source {[type]} -- [description]
            target {[type]} -- [description]

    Raises:
        exceptions.ContentsCacheExpired: [description]

    Returns:
        [type] -- [description]
    """
    contentscache_obj = get_contents_cache_obj(**kwargs)
    if contentscache_obj is False:
        return False
    if check_contents_cache_expired(contentscache_obj) is False:
        raise exceptions.ContentsCacheExpired
    return contentscache_obj


def check_contents_cache_expired(contentscache_obj):
    expire_datetime = contentscache_obj.createtime + timedelta(**CACHE_EXPIRED_TIMEDELTA)
    if datetimenow() >= expire_datetime:
        return False
    return True


def create_contents_cache(**kwargs):
    """Create ContentsCache Object

    Arguments:
        **kwargs
            * contentshash_obj {ContentsHash Object} -- ContentsHash Object
            * vendor {str} -- [description]
            * source {str} -- [description]
            * target {str} -- [description]
            * translated_text {str} -- [description]

    Returns:
        ContentsCache -- ContentsCache Object
    """
    contentscache_obj = ContentsCache()
    contentscache_obj.contents_hash = kwargs['contentshash_obj']
    contentscache_obj.vendor = kwargs['vendor']
    contentscache_obj.source = kwargs['source']
    contentscache_obj.target = kwargs['target']
    contentscache_obj.translated_text = kwargs['translated_text']
    contentscache_obj.save()
    if contentscache_obj.seq:
        return contentscache_obj
    else:
        return False

def update_contents_cache(**kwargs):
    """[summary]

    Arguments:
        **kwargs
            contentshash_obj {[type]} -- [description]
            vendor {[type]} -- [description]
            source {[type]} -- [description]
            target {[type]} -- [description]
            translated_text {[type]} -- [description]

    Raises:
        exceptions.ContentsCacheNotExists: [description]

    Returns:
        [type] -- [description]
    """
    contentscache_obj = get_contents_cache_obj(**kwargs)
    if not contentscache_obj:
        raise exceptions.ContentsCacheNotExists
    contentscache_obj.translated_text = kwargs['translated_text']
    contentscache_obj.createtime = datetimenow()
    contentscache_obj.save()
    return contentscache_obj

def create_or_update_contents_cache(**kwargs):
    """[summary]

    Arguments:
        **kwargs
            contentshash_obj {[type]} -- [description]
            vendor {[type]} -- [description]
            source {[type]} -- [description]
            target {[type]} -- [description]
            translated_text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    try:
        contentscache_obj = update_contents_cache(**kwargs)
    except exceptions.ContentsCacheNotExists:
        contentscache_obj = create_contents_cache(**kwargs)
        if contentscache_obj is False:
            return False
    return contentscache_obj