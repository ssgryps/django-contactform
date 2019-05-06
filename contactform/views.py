from django.shortcuts import get_object_or_404, render

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
            return render(request, "contactform/base.html", context=context)
        else:
            # error happened
            context = {
                'form': form,
                'form_model': contact_form,
                'success': False,
            }
            return render(request, "contactform/base.html", context=context)
    else:
        form = FormClass()
    context = {
        'form': form,
        'form_model': contact_form,
        'success': False,
    }
    return render(request, "contactform/base.html", context=context)
