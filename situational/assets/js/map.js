(function (window, $, L) {
  'use strict';

  $('.leaflet-map').each(function () {
    var $this = $(this),
      latitude = $this.data('latitude'),
      longitude = $this.data('longitude'),
      map;

    if ($.isNumeric(latitude) && $.isNumeric(longitude)) {
      map = L.map(this, {
        center: [latitude, longitude],
        zoom: 12,
        dragging: false,
        touchZoom: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        boxZoom: false,
        tap: false,
        zoomControl: false
      });

      L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
      }).addTo(map);

    } else {
      $this.data("mapError", "Couldn't parse lat/long as a number");
    }
  });

}(this, jQuery, L));
