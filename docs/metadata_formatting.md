# Fields obtainable through Crossref API
title - string
institution_names - list of strings # institutions (e.g. universities) of authors
publication_name - string  # journal name if a journal, book name if book
publish_date - list of integers  # length 3, first element for year, 2nd for month, 3rd for day, if any value not available it's set to 0
type - string  # type of publication (e.g. book, journal, etc.)
abstract - string
DOI - string
URL_link - string
authors - list of strings
references - list of strings  # DOI numbers for references
# other fields through elsevier API
scopus_id - string
section_titles - list of strings  # names for the titles of the paper sections
fig_captions - list of strings  # caption text for figures (useful?)
keywords - list of strings  # keywords provided by the article
# semantics API (to be filled)