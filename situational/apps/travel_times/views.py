from django.http import HttpResponse
from django.views.generic import View

from .models import TravelTimesMap


class MapView(View):
    default_width = '1200'
    default_height = '1200'
    default_depart_at = '0800'

    def get(self, request, *args, **kwargs):
        postcode = kwargs.get('postcode')
        width = request.GET.get('width', self.default_width)
        height = request.GET.get('height', self.default_height)

        travel_map, _created = TravelTimesMap.objects.get_or_create(
            postcode=postcode,
            width=width,
            height=height,
        )
        if not travel_map.has_image:
            travel_map.download_image()

        return HttpResponse(travel_map.read_image(), travel_map.mime_type)
