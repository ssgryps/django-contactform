# -*- coding: utf-8 -*-


from django.db import models, migrations
import contactform.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'de', b'German')])),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='title', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('submit_label', models.CharField(help_text='Standard: "submit"', max_length=30, verbose_name='submit label', blank=True)),
                ('success_message', models.TextField(verbose_name='success message', blank=True)),
                ('cc_managers', models.BooleanField(default=False, help_text='Check to send a copy to the site managers ().', verbose_name='CC to managers')),
                ('cc_site_contact', models.BooleanField(default=False, help_text='Check to send a copy to the site contact (<function _site_contact_email at 0x7f52a7681de8>).', verbose_name='CC to site contact')),
                ('has_captcha', models.BooleanField(default=False, help_text='Should the user be required to fill up a captcha to verify he is human?', verbose_name='has a captcha')),
                ('css_class', models.CharField(max_length=255, null=True, verbose_name='CSS class', blank=True)),
                ('notification_email_subject', models.CharField(max_length=200, verbose_name='notification email subject', blank=True)),
                ('notification_email_body', models.TextField(verbose_name='notification email body', blank=True)),
            ],
            options={
                'verbose_name': 'contact form',
                'verbose_name_plural': 'contact forms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactFormIntermediate',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=models.CASCADE)),
                ('form', models.ForeignKey(verbose_name='form', to='contactform.ContactForm', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContactFormSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='submit date/time')),
                ('sender_ip', models.CharField(max_length=40, verbose_name='sender IP address')),
                ('form_url', models.URLField(verbose_name='form URL')),
                ('language', models.CharField(default=b'unknown', max_length=255, verbose_name='language')),
                ('form_data', models.TextField(null=True, verbose_name='form data', blank=True)),
                ('form_data_pickle', contactform.fields.PickledObjectField(verbose_name='form data pickle', null=True, editable=False, blank=True)),
                ('form', models.ForeignKey(to='contactform.ContactForm', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-submitted_at',),
                'verbose_name': 'contact form submission',
                'verbose_name_plural': 'contact form submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactFormSubmissionAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'private/contactform/submissions/%Y-%m-%d', max_length=200, verbose_name='file')),
                ('submission', models.ForeignKey(related_name='attachments', verbose_name='submission', to='contactform.ContactFormSubmission', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'contact form submission attachment',
                'verbose_name_plural': 'contact form submission attachments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name='label')),
                ('field_type', models.CharField(max_length=100, verbose_name='field type', choices=[(b'django.forms.CharField', 'character field'), (b'django.forms.EmailField', 'email field'), (b'django.forms.BooleanField', 'checkbox'), (b'django.forms.ChoiceField', 'choice field'), (b'django.forms.FileField', 'file field'), (b'contactform.forms.EmailWithConfirmation', 'send confirmation to user email field'), (b'contactform.forms.EmailWithConfirmationCheckbox', 'send confirmation to user checkbox')])),
                ('widget', models.CharField(blank=True, max_length=50, verbose_name='widget', choices=[(b'django.forms.Textarea', 'textarea'), (b'django.forms.PasswordInput', 'password input'), (b'django.forms.RadioSelect', 'radio buttons')])),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('initial', models.CharField(max_length=64, null=True, verbose_name='initial', blank=True)),
                ('choices', models.TextField(help_text='enter choices divided by a semicolon (;) for ChoiceFields', null=True, verbose_name='choices', blank=True)),
                ('css_class', models.CharField(max_length=255, null=True, verbose_name='CSS class', blank=True)),
                ('position', models.IntegerField(default=1, verbose_name='position')),
                ('form', models.ForeignKey(related_name='field_set', to='contactform.ContactForm', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email')),
            ],
            options={
                'verbose_name': 'recipient',
                'verbose_name_plural': 'recipients',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contactform',
            name='recipients',
            field=models.ManyToManyField(to='contactform.Recipient', verbose_name='recipients'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactform',
            name='success_page',
            field=models.ForeignKey(blank=True, to='cms.Page', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
