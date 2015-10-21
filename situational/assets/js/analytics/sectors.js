var trackKeywordCount = function(num_keywords) {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'sectors', 'KeywordsSearched', 'number_keywords', num_keywords);
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}

var trackKeyword = function(keyword) {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'sectors', 'Keyword', keyword);
  } else {
    console.log("GoogleAnalytics not available in debug mode.")
  }
}
