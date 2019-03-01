from django.conf import settings
from django.contrib import admin

from contactform.models import ContactForm, Recipient, FormField, ContactFormSubmission,\
    ContactFormSubmissionAttachment

class FormFieldInline(admin.TabularInline):
    model = FormField
    num_in_admin = 4 
    extra = 4 

class ContactFormAdmin(admin.ModelAdmin):
    inlines = [
        FormFieldInline,
    ]
    if 'captcha' not in settings.INSTALLED_APPS:
        exclude = ('has_captcha',)
    list_display = ('name', 'language',)
    list_filter = ('language',)
    search_fields = ('name',)
    ordering = ('id', 'language',)
    save_as = True

    class Media:
        css = {
            "all": ("contactform/css/contactform_admin.css",)
        }

class ContactFormSubmissionAttachmentAdmin(admin.TabularInline):
    model = ContactFormSubmissionAttachment
    extra = 0

class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'submitted_at', 'language', 'sender_ip',)
    list_filter = ('form', 'language', 'submitted_at')
    search_fields = ('form_data',)
    date_hierarchy = 'submitted_at'
    inlines = [
        ContactFormSubmissionAttachmentAdmin,
    ]
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            (r'^csv/$', 'contactform.csv_export_views.export'),
        )
        return urlpatterns + super(ContactFormSubmissionAdmin, self).get_urls()

admin.site.register(ContactForm, ContactFormAdmin)
admin.site.register(Recipient)
admin.site.register(ContactFormSubmission, ContactFormSubmissionAdmin)