# -*- coding: utf-8 -*-
from . import l_request


def request(url, retries=5, callback=None, **kwargs):
    with l_request.LRequest() as lrequest:
        return lrequest.request(url, retries, callback, **kwargs)
    pass


