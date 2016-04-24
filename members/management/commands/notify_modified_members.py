import reversion

from datetime import date, timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import Context, Template

from members.models import Member


email_template = """\
{% load getattribute %}Hello everyone,

Here are the modified and created user entries from yesterday :
{% for entry, users in data.created %}
'{{ entry.object }}' created by {{ users }}:
{% for field in fields|only_existing:entry %}* {% if field.verbose_name %}{{ field.verbose_name|safe }}{% else %}{{ field.name }}{% endif %}: {{ entry|get_field:field }}
{% endfor %}{% endfor %}
{% for new, old, users in data.modified %}
'{{ new.object }}' modified by {{ users }}:
{% for field in new|only_modified:old %}* {% if field.verbose_name %}{{ field.verbose_name|safe }}{% else %}{{ field.name }}{% endif %}: '{{ old|get_field:field }}' -> '{{ new|get_field:field }}'
{% endfor %}{% endfor %}

Thanks for your work <3
"""


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        data = {
            "created": [],
            "modified": [],
        }

        today = date.today()
        yesterday = today - timedelta(days=1)
        modified_yesterday_members = Member.objects.filter(last_modified__lt=date.today(), last_modified__gt=yesterday)

        for member_revisions in map(reversion.get_for_object, modified_yesterday_members):
            member_revisions = list(member_revisions.get_unique())

            old_data = filter(lambda x: x.field_dict["last_modified"] is None, member_revisions)
            member_revisions = filter(lambda x: x.field_dict["last_modified"] is not None, member_revisions)

            # old data
            if not member_revisions:
                continue

            yesterday_modifications = filter(lambda x: x.field_dict["last_modified"].date() == yesterday, member_revisions)

            users_that_has_modified_the_documented = u", ".join(set(map(lambda x: unicode(x.revision.user), yesterday_modifications)))

            if old_data and len(member_revisions) == 1:
                data["modified"].append([yesterday_modifications[0], old_data[0], users_that_has_modified_the_documented])
                continue

            older_modifications = filter(lambda x: x.field_dict["last_modified"].date() < yesterday, member_revisions)
            if not older_modifications:
                data["created"].append([yesterday_modifications[0], users_that_has_modified_the_documented])
            else:
                data["modified"].append([yesterday_modifications[0], older_modifications[0], users_that_has_modified_the_documented])

        if not data["created"] and not data["modified"]:
            # don't send empty email
            return

        fields = filter(lambda x: x.name not in ('added_on', 'last_modified', 'id', 'pk'), Member._meta.fields)

        email_content = Template(email_template).render(Context({
            "data": data,
            "fields": fields,
        }))

        send_mail('[NeutrinetMembersManangement] modifications of %s' % yesterday.strftime("%F"), email_content, 'noreply@neutrinet.be', ['administration@neutrinet.be'], fail_silently=False)
