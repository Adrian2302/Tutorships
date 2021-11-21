from django import template
import urllib.parse

from Tutorship.models import RequestNotification
from UserAuthentication.models import User

register = template.Library()



@register.inclusion_tag('showNotifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    user = User.objects.get(id=request_user.id)
    notifications = RequestNotification.objects.filter(to_user=user, seen=False).order_by('-date')
    return {'notifications': notifications}

@register.filter
def toggle_value(request, arg):
    url_parts = list(urllib.parse.urlparse(request.get_full_path()))
    print(url_parts[4])
    query = dict(urllib.parse.parse_qsl(url_parts[4], keep_blank_values=True))
    query["pagina"] = arg
    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)
  
