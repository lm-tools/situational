function trackKeywordCount(num_keywords) {
  ga('send', 'event', 'sectors', 'KeywordsSearched', 'number_keywords', num_keywords);
}

function trackKeyword(keyword) {
  ga('send', 'event', 'sectors', 'Keyword', keyword);
}

function trackSocCodeClicked(keyword, soc_code) {
  ga(
    'send',
    'event',
    'sectors',
    'SocCodeClicked',
    keyword,
    1,
    {
      soc_code: soc_code
    }
  )
}
