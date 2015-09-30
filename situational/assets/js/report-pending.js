(function (window, $) {
  'use strict';

  var $resultFields, resultFieldsLength, resultFieldsUrl, updateIntervalId;

  $resultFields = $(".result-field");
  resultFieldsLength = $resultFields.length;
  resultFieldsUrl = window.location.pathname + "/populated_result_fields.json";

  function updateResults() {
    $.getJSON(resultFieldsUrl)
      .done(updateResultFields);
  }

  function updateResultFields(populatedFields) {
    var allFieldsPopulated = true;
    $resultFields.each(function () {
      var $this = $(this),
        isPopulated = (populatedFields.indexOf($this.data("resultFieldName")) != -1);
      $(this).toggleClass("result-field--populated", isPopulated);
      $(this).toggleClass("populated", isPopulated);
      allFieldsPopulated = allFieldsPopulated && isPopulated;
    });
    if (allFieldsPopulated) {
      window.clearInterval(updateIntervalId);
      window.location.reload();
    }
  }

  if (resultFieldsLength > 0) {
    updateIntervalId = window.setInterval(updateResults, 250);
  }
}(this, jQuery));
