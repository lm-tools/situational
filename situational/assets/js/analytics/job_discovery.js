var trackJobApplication = function() {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'job_discovery', 'apply');
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}
