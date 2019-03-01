from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from contactform.models import ContactForm

def index(request, form_model_id):
    contact_form = get_object_or_404(ContactForm, pk=form_model_id)
    FormClass = contact_form.get_form_class()
    if request.method == "POST":
        form = FormClass(request.POST, request.FILES)
        if form.is_valid() and form.handle_submission(request):
            # form was processed sucessfully
            context = {
                'form': form,
                'form_model': contact_form,
                'success': True,
            }
            return render_to_response("contactform/base.html", dictionary=context, context_instance=RequestContext(request))
        else:
            # error happened
            context = {
                'form': form,
                'form_model': contact_form,
                'success': False,
            }
            return render_to_response("contactform/base.html", dictionary=context, context_instance=RequestContext(request))
    else:
        form = FormClass()
    context = {
        'form': form,
        'form_model': contact_form,
        'success': False,
    }
    return render_to_response("contactform/base.html", dictionary=context, context_instance=RequestContext(request))
