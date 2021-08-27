# -*- coding: utf-8 -*-

import os
import json
import platform
import time
import django
from django import template
from django.utils.html import format_html
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db import models
from django.templatetags import static



register = template.Library()


@register.filter
def get_icon(name):
    # 默认为文件图标
    cls = ""
    return format_html('<i class="icon {}"></i>', cls)


@register.simple_tag(takes_context=True)
def load_dates(context):
    data = {}
    cl = context.get('cl')
    if cl.has_filters:
        for spec in cl.filter_specs:
            field = spec.field
            field_type = None
            if isinstance(field, models.DateTimeField):
                field_type = 'datetime'
            elif isinstance(field, models.DateField):
                field_type = 'date'
            elif isinstance(field, models.TimeField):
                field_type = 'time'

            if field_type:
                data[field.name] = field_type
    context['date_field'] = data

    return '<script type="text/javascript">var searchDates={}</script>'.format(json.dumps(data))


@register.filter
def get_date_type(spec):
    field = spec.field
    field_type = ''
    if isinstance(field, models.DateTimeField):
        field_type = 'datetime'
    elif isinstance(field, models.DateField):
        field_type = 'date'
    elif isinstance(field, models.TimeField):
        field_type = 'time'

    return field_type

 

@register.filter
def to_str(obj):
    return str(obj)


@register.filter
def date_to_json(obj):
    return json.dumps(obj.date_params)


@register.simple_tag(takes_context=True)
def home_page(context):
    '''
    处理首页，通过设置判断打开的是默认页还是自定义的页面
    :return:
    '''
    home = __get_config('SIMPLEUI_HOME_PAGE')
    if home:
        context['home'] = home

    title = __get_config('SIMPLEUI_HOME_TITLE')
    if not title:
        title = '首页'

    icon = __get_config('SIMPLEUI_HOME_ICON')
    if not icon:
        icon = 'el-icon-menu'

    context['title'] = title
    context['icon'] = icon

    return ''


def __get_config(name):
    value = os.environ.get(name, getattr(settings, name, None))
    return value


@register.filter
def get_config(key):
    return __get_config(key)


@register.simple_tag
def get_server_info():
    dict = {
        'Network': platform.node(),
        'OS': platform.platform(),
    }
    return format_table(dict)


@register.simple_tag
def get_app_info():
    dict = {
        'Python': platform.python_version(),
        'Django': django.get_version()
    }

    return format_table(dict)


def format_table(dict):
    html = '<table class="simpleui-table"><tbody>'
    for key in dict:
        html += '<tr><th>{}</th><td>{}</td></tr>'.format(key, dict.get(key))
    html += '</tbody></table>'
    return format_html(html)

@register.simple_tag(takes_context=True)
def plots(context):
    apps = context.get('app_list')
    result = []
    for app in apps:
        for model in app.get('models', []):
            plots = model.get('plots')
            if plots:
                for plot in plots:
                    result.append('''
                                <el-col :span="{}" style="padding:30px;">{}</el-col>
                        '''.format(plot.get('size'), plot.get('plot')))
    return mark_safe(''.join(result))


@register.simple_tag(takes_context=True)
def menus(context):
    data = []
    config = get_config('SIMPLEUI_CONFIG')
    app_list = context.get('app_list')
    for app in app_list:
        models = []
        if app.get('models'):
            for m in app.get('models'):
                models.append({
                                'name': str(m.get('name')),
                                'icon': get_icon(m.get('object_name')),
                                'url': m.get('admin_url'),
                                'addUrl': m.get('add_url'),
                                'breadcrumbs': [str(app.get('name')), str(m.get('name'))]
                             })
        module = {
                    'name': str(app.get('name')),
                    'icon': get_icon(app.get('app_label')),
                    'models': models
                } 
        data.append(module)

    # 如果有menu 就读取，没有就调用系统的
    if config and 'menus' in config:
        if 'system_keep' in config:
            temp = config.get('menus')
            for i in temp:
                data.append(i)
        else:
            data = config.get('menus')
     
    return '<script type="text/javascript">var menus={}</script>'.format(json.dumps(data))



def get_icon(obj):
    dict = {
        'auth': 'fas fa-shield-alt',
        'User': 'far fa-user',
        'Group': 'fas fa-users-cog',
        'market': 'fas fa-shopping-bag',
        'account': 'fas fa-user-circle',
        'Buyed':'fas fa-shopping-cart',
        'BuyedDetail':'fas fa-shopping-basket',
        'Header':'fas fa-shopping-bag',
        'Category':'fas fa-sun',
        'Promo':'fas fa-shopping-bag',
        'Album':'fas fa-id-badge',
        'Feedback':'fas fa-phone-square',
        'FlashSale':'fas fa-lightbulb',
        'Group':'fas fa-user-circle',
        'UserProfile':'fas fa-user',
        'Panel':'fas fa-adjust',
        'Tips':'fas fa-bell',
        'Area':'fas fa-cloud',
        'Plan':'fas fa-paper-plane',
        'Company':'fas fa-compass',
        'Account':'fas fa-user-circle',
        'Contract':'fas fa-folder-open',
        'Order':'fas fa-tags',
        'Config':'fas fa-address-book',
        'distribution':'fas fa-tablet',
        'DPanel':'fas fa-adjust',
        'UserCategory':'far fa-user',
        'UserCapital':'fas fa-adjust',
        'crm':'fas fa-sun',
        'Permission':'fas fa-lightbulb'
    }
     
    temp = dict.get(obj)
    if not temp:
        return 'fas fa-sun'
    return temp


@register.simple_tag(takes_context=True)
def load_message(context):
    messages = context.get('messages')
    array = []
    if messages:
        for msg in messages:
            array.append({
                            'msg': msg.message,
                            'tag': msg.tags
                        })

    return '<script type="text/javascript"> var messages={}</script>'.format(array)


@register.simple_tag(takes_context=True)
def context_to_json(context):
    json_str = '{}'
    return mark_safe(json_str)


@register.simple_tag()
def get_language():
    x = django.utils.translation.get_language()
    return x


@register.filter
def get_language_code(val):
    x = django.utils.translation.get_language()
    return x


def get_analysis_config():
    val = __get_config('SIMPLEUI_ANALYSIS')
    if not val and val == False:
        return False
    return True


@register.simple_tag(takes_context=True)
def load_analysis(context):
    try:
        html =''
        return mark_safe(html)
    except:
        return ''
