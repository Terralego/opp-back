from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from terra_opp.models import Campaign
from terra_opp.serializers import CampaignSerializer


campaign_updated_templates = {
    "text": "notifications/campaign_updated.txt",
    "html": "notifications/campaign_updated.html",
}

@api_view(['get'])
def notify_admin(request, pk=None, *args, **kwargs):
    campaign = Campaign.objects.get(pk=pk)

    # sending email to admin
    context = {
        "url": f"{settings.FRONT_ADMIN_URL}/campaign/{campaign.id}",
        "title": settings.TROPP_OBSERVATORY_TITLE,
        "campaign": campaign,
    }

    txt = render_to_string(campaign_updated_templates["text"], context)
    html = render_to_string(campaign_updated_templates["html"], context)

    raw_subject = _(
        "New photographs submitted for validation - {campaign}"
    ).format(campaign=campaign.label)

    subject = f"[{settings.TROPP_OBSERVATORY_SHORT_TITLE}] {raw_subject}"

    send_mail(
        subject,
        txt,
        settings.DEFAULT_FROM_EMAIL,
        [campaign.owner.email],
        html_message=html,
        fail_silently=False,
    )

    # Return response to front-end
    serializer = CampaignSerializer(campaign)
    return Response(status=status.HTTP_200_OK, data=serializer.data)
