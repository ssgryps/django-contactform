from django.utils.translation import ugettext_lazy as _

from cms import __version__ as cms_version
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from contactform.models import ContactFormIntermediate


class ContactFormPlugin(CMSPluginBase):
    model = ContactFormIntermediate
    name = _("Contact Form")
    render_template = "contactform/form.html"
    change_form_template = "contactform/plugin_form.html"

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        We override the change form template path
        to provide backwards compatibility with CMS 2.x
        """
        if cms_version.startswith('2'):
            context['change_form_template'] = "admin/cms/page/plugin_change_form.html"
        return super(ContactFormPlugin, self).render_change_form(request, context, add, change, form_url, obj)

    def render(self, context, instance, placeholder):
        request = context['request']

        contact_form = instance.form
        FormClass = contact_form.get_form_class(unique_form_id=instance.pk)

        context['instance'] = instance
        context['placeholder'] = placeholder
        context['form_model'] = contact_form


        if request.method == "POST" and request.POST.get('unique_form_id', None) == str(instance.pk):
            form = FormClass(request.POST, request.FILES)
            if form.is_valid() and form.handle_submission(request):
                # form was processed sucessfully
                if instance.form.success_page:
                    context['redirect'] = instance.form.success_page.get_absolute_url()
                context['form'] = form
                context['success'] = True
            else:
                context['form'] = form
                context['success'] = False
        else:
            context['form'] = FormClass()
            context['success'] = False

        return context

plugin_pool.register_plugin(ContactFormPlugin)