"""
Common template tags to reduce duplication in templates.
"""
from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.inclusion_tag('snippets/breadcrumb.html')
def render_breadcrumb(items):
    """
    Render breadcrumb navigation.
    
    Usage: {% render_breadcrumb breadcrumb_items %}
    where breadcrumb_items is a list of {'title': 'Name', 'url': 'url_name'} dicts
    """
    return {'items': items}


@register.inclusion_tag('snippets/form_errors.html')
def render_form_errors(form):
    """
    Render form errors consistently.
    
    Usage: {% render_form_errors form %}
    """
    return {'form': form}


@register.inclusion_tag('snippets/pagination.html')
def render_pagination(page_obj):
    """
    Render pagination controls.
    
    Usage: {% render_pagination page_obj %}
    """
    return {'page_obj': page_obj}


@register.simple_tag
def standard_button(text, btn_type='primary', icon=None, url=None):
    """
    Generate standard buttons.
    
    Usage: {% standard_button "Add New" "primary" "fas fa-plus" %}
    """
    icon_html = f'<i class="{icon}"></i> ' if icon else ''
    if url:
        return f'<a class="btn btn-{btn_type}" href="{url}">{icon_html}{text}</a>'
    else:
        return f'<button type="submit" class="btn btn-{btn_type}">{icon_html}{text}</button>'


@register.filter
def get_verbose_name(obj, field_name):
    """
    Get verbose name of a model field.
    
    Usage: {{ object|get_verbose_name:"field_name" }}
    """
    return obj._meta.get_field(field_name).verbose_name


@register.simple_tag
def alert_message(message_type, message):
    """
    Generate alert messages consistently.
    
    Usage: {% alert_message "success" "Operation completed successfully" %}
    """
    icon_map = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-triangle',
        'warning': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    }
    icon = icon_map.get(message_type, 'fas fa-info-circle')
    return f'''
    <div class="alert alert-{message_type} alert-dismissible fade show" role="alert">
        <i class="{icon} me-2"></i>{message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    '''