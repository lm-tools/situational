from django.views.generic import TemplateView

from job_discovery.adzuna import Adzuna


class JobCardsView(TemplateView):
    template_name = "job_discovery/job_cards.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        az = Adzuna()
        context['jobs'] = az.jobs_at_location(
            'UK',
            'London',
            'Central London',
            50
        )
        return context
