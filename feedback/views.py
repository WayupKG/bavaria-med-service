from random import randint

from django.views.generic import FormView

from core.mixins import ViewMixin

from .models import Recaptcha
from .forms import CreateStatementForm
from feedback import pages_info as info

    
class ContactView(FormView):
    form_class = CreateStatementForm
    template_name = 'contact.html'
    success_url = '/contacts/thanks/'

    @staticmethod
    def get_recaptcha(**kwargs):
        count = Recaptcha.objects.all().count()
        return Recaptcha.objects.all()[randint(0, int(count) - 1)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = info.contact_title
        context["description"] = info.contact_description
        context["recaptcha"] = self.get_recaptcha()
        context["errors"] = False if not kwargs.get('errors') else True
        return context

    def form_valid(self, form):
        data = self.request.POST.get
        if int(data('answer_user')) == int(data('answer_recaptcha')):
            form.save()
            form.send_statement()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(errors=True))


class ThanksView(ViewMixin):
    title = 'Спасибо за заявку!'
    description = 'Наш консультант перезвонит вам в течение нескольких часов.'
    template_name = 'email/success_send_statement.html'