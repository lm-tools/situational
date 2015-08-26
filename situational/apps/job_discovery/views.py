from django.views.generic import TemplateView


class JobCardsView(TemplateView):
    template_name = "job_discovery/job_cards.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
