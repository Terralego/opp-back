from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from terra_opp.models import Campaign, Picture
from terra_opp.signals import state_change

campaign_started_templates = {
    "text": "notifications/campaign_started.txt",
    "html": "notifications/campaign_started.html",
}

picture_submitted_templates = {
    "text": "notifications/picture_submitted.txt",
    "html": "notifications/picture_submitted.html",
}

picture_refused_templates = {
    "text": "notifications/picture_refused.txt",
    "html": "notifications/picture_refused.html",
}

campaign_updated_templates = {
    "text": "notifications/campaign_updated.txt",
    "html": "notifications/campaign_updated.html",
}


@receiver(state_change, sender=Campaign)
def send_campaign_notifications(
    sender, instance=None, prev_state=None, new_state=None, **kwargs
):

    if new_state == Campaign.STARTED:
        context = {
            "url": f"{settings.FRONT_ADMIN_URL}/campaign/{instance.id}",
            "title": settings.TROPP_OBSERVATORY_TITLE,
            "campaign": instance,
        }

        txt = render_to_string(campaign_started_templates["text"], context)
        html = render_to_string(campaign_started_templates["html"], context)

        raw_subject = _(
            "A new re-photography campaign has been assigned to you: {campaign}"
        ).format(campaign=instance.label)

        subject = f"[{settings.TROPP_OBSERVATORY_SHORT_TITLE}] {raw_subject}"

        send_mail(
            subject,
            txt,
            settings.DEFAULT_FROM_EMAIL,
            [instance.assignee.email],
            html_message=html,
            fail_silently=False,
        )


@receiver(state_change, sender=Picture)
def send_picture_submitted(
    sender, instance=None, prev_state=None, new_state=None, **kwargs
):

    if new_state == Picture.SUBMITTED:
        context = {
            "url": f"{settings.FRONT_ADMIN_URL}/picture/{instance.id}",
            "title": settings.TROPP_OBSERVATORY_TITLE,
            "campaign": instance.campaign,
            "viewpoint": instance.viewpoint,
        }

        txt = render_to_string(picture_submitted_templates["text"], context)
        html = render_to_string(picture_submitted_templates["html"], context)

        raw_subject = _(
            "New photograph submitted for validation - {campaign}: {viewpoint}"
        ).format(campaign=instance.campaign.label, viewpoint=instance.viewpoint.label)

        subject = f"[{settings.TROPP_OBSERVATORY_SHORT_TITLE}] {raw_subject}"

        send_mail(
            subject,
            txt,
            settings.DEFAULT_FROM_EMAIL,
            [instance.campaign.owner.email],
            html_message=html,
            fail_silently=False,
        )


@receiver(state_change, sender=Picture)
def send_picture_refused(
    sender, instance=None, prev_state=None, new_state=None, **kwargs
):

    if new_state == Picture.REFUSED:
        context = {
            "url": f"{settings.FRONT_ADMIN_URL}/campaign/{instance.campaign.id}",
            "title": settings.TROPP_OBSERVATORY_TITLE,
            "campaign": instance.campaign,
            "viewpoint": instance.viewpoint,
            "reason": instance.properties.get("refusal_message", "-"),
        }

        txt = render_to_string(picture_refused_templates["text"], context)
        html = render_to_string(picture_refused_templates["html"], context)

        raw_subject = _("Photograph rejected - {campaign}: {viewpoint}").format(
            campaign=instance.campaign.label, viewpoint=instance.viewpoint.label
        )

        subject = f"[{settings.TROPP_OBSERVATORY_SHORT_TITLE}] {raw_subject}"

        send_mail(
            subject,
            txt,
            settings.DEFAULT_FROM_EMAIL,
            [instance.campaign.assignee.email],
            html_message=html,
            fail_silently=False,
        )
