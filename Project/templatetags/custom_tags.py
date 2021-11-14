from django import template
from Tutorship.models import RequestNotification
from UserAuthentication.models import User

register = template.Library()


@register.inclusion_tag('showNotifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    user = User.objects.get(id=request_user.id)
    notifications = RequestNotification.objects.filter(to_user=user, seen=False).order_by('-date')
    return {'notifications': notifications}
