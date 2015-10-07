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
        dragging: false
      });

      L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
      }).addTo(map);

      var circle = L.circle([latitude, longitude], 750, {
        color: '#007095',
        fillColor: '#008CBA',
        fillOpacity: 0.5
      }).addTo(map);

    } else {
      $this.data("mapError", "Couldn't parse lat/long as a number");
    }
  });

}(this, jQuery, L));
