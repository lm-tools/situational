(function (window, $) {
  'use strict';

  var isPopulated, isPopulatedUrl, updateIntervalId;
  isPopulatedUrl = window.location.pathname + "/is_populated.json";

  function updateReport() {
    $.getJSON(isPopulatedUrl)
      .done(reloadIfPopulated);
  }

  function reloadIfPopulated(is_populated_json) {
    if (is_populated_json) {
      window.clearInterval(updateIntervalId);
      window.location.reload();
    }
  }

  if (!isPopulated) {
    updateIntervalId = window.setInterval(updateReport, 250);
  }
}(this, jQuery));
