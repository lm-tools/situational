var sendReportEmail = function(tool_name) {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', tool_name, 'report_email');
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}
