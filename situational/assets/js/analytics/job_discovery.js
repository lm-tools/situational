var trackJobApplication = function() {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'job_discovery', 'apply');
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}

var viewDiscoveryReport = function(liked, disliked) {
  if (typeof ga !== 'undefined') {
    ga(
      'send',
      'event',
      'job_discovery',
      'view_report',
      'JobsSaved',
      liked+disliked,
      {
        liked: liked,
        disliked: disliked
      }
    );
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}
