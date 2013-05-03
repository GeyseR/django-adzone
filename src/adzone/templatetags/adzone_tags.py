# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime
from django import template
from adzone.models import AdBase, AdImpression
from django.utils import six

register = template.Library()


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_zone_ad(context, ad_zone, cnt=1):
    """
    Returns a random advert for ``ad_zone``.
    The advert returned is independent of the category

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'adzone.context_processors.get_source_ip'

    Tag usage:
    {% load adzone_tags %}
    {% random_zone_ad 'zone_slug' %}

    """
    to_return = {'ad_zone': ad_zone, 'ad_category': None}

    # Retrieve a random ad for the zone
    ad = AdBase.objects.get_random_ad(ad_zone)[0]
    to_return['ad'] = ad

    # Record a impression for the ad
    if 'from_ip' in context and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip)
            impression.save()
        except:
            pass
    return to_return


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_category_ad(context, ad_zone, ad_category, cnt=1):
    """
    Returns a random advert from the specified category.

    Usage:
    {% load adzone_tags %}
    {% random_category_ad 'zone_slug' 'my_category_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    ad = AdBase.objects.get_random_ad(ad_zone, ad_category)[0]
    to_return['ad'] = ad

    # Record a impression for the ad
    if 'from_ip' in context and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip)
            impression.save()
        except:
            pass
    return to_return


@register.assignment_tag(takes_context=True)
def random_many_ad(context, ad_zone, ad_category=None, cnt=1):
    """
    Returns a queryset with random adverts for specified zone and
    from the specified category if passed.
    Write AdImpression for all returned adverts

    Usage:
    {% load adzone_tags %}
    {% random_many_ad ad_zone='zone_slug' ad_category='my_category_slug' cnt=5 as ad_qs %}

    """

    ad_qs = AdBase.objects.get_random_ad(ad_zone, ad_category, cnt)

    from_ip = context.get('from_ip')
    if from_ip:
        for ad in ad_qs:
            try:
                impression = AdImpression(
                    ad=ad, impression_date=datetime.now(), source_ip=from_ip)
                impression.save()
            except:
                pass

    return ad_qs