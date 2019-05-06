"""
converts all the existing saved contact form submission data into the new
pickle format, so it can be used for csv export and stuff
"""

from contactform.models import ContactFormSubmission
from django.template.defaultfilters import slugify
import re

subs = ContactFormSubmission.objects.all()


def doit():
    for sub in subs:
        if sub.form_data_pickle in (None, {}, ''):
            to_pickle = {}
            manipulated = str(sub.form_data).replace('\r\n', '------xxxxx-----')
            r = re.findall(r"\n([^:\n\r]+): (.+)\n", manipulated, re.MULTILINE)
            for key, value in r:
                if not key.lower() in ['formularname', 'form url']:
                    to_pickle[str(slugify(key))] = str(value).replace('------xxxxx-----', '\r\n')
            sub.form_data_pickle = to_pickle
            sub.save()
doit()