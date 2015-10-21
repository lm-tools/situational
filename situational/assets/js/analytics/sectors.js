function trackKeywordCount(num_keywords) {
  ga('send', 'event', 'sectors', 'KeywordsSearched', 'number_keywords', num_keywords);
}

function trackKeyword(keyword) {
  ga('send', 'event', 'sectors', 'Keyword', keyword);
}
