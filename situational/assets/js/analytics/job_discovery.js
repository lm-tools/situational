function trackJobApplication() {
  ga('send', 'event', 'job_discovery', 'apply');
}

function trackViewDiscoveryReport(liked, disliked) {
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
}
