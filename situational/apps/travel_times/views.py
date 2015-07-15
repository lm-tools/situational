from django.http import HttpResponse
from django.views.generic import View

from travel_times.models import TravelTimesMapRepository


class MapView(View):
    default_width = '1200'
    default_height = '1200'
    default_depart_at = '0800'

    def get(self, request, *args, **kwargs):
        postcode = kwargs.get('postcode')
        width = request.GET.get('width', self.default_width)
        height = request.GET.get('height', self.default_height)

        repo = TravelTimesMapRepository()
        travel_map = repo.get(postcode, width, height)

        return HttpResponse(travel_map.read_image(), travel_map.mime_type)
