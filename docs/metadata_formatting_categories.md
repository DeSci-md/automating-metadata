# Paper Identification
DOI - string, crossref
scopus_id - string, elsevier, returns "None" if error
paperId - string, semantic  # identification from Semantics scholar API
title - string, crossref
publication_name - string, crossref  # journal name if a journal, book name if book
publish_date - list of integers, crossref  # length 3, first element for year, 2nd for month, 3rd for day, if any value not available it's set to 0

# Paper Categorization
type - string, crossref  # type of publication (e.g. book, journal, etc.)
keywords - list of strings, elsevier  # keywords provided by the article, returns "None" if error
subject - list of strings, crossref # keywords provided by Crossref for the article
fields_of_study - list of strings, semantic  # field of study keywords returned by Semantic Scholar

# Connections between people and groups
authors - list of strings, crossref
institution_names - list of strings, crossref # institutions (e.g. universities) of authors
references - list of strings, crossref  # DOI numbers for references

# Paper content and accessing methods
tldr - string, semantic  # auto generated summary from https://github.com/allenai/scitldr model if available, return "null" string if not
abstract - string, Elsevier, returns "None" if error
original_text - string, Elsevier # paper text in full, if available, return None if not
openAccessPdf - string, semantic  # URL to web PDF if the publication is open Access
URL_link - string, crossref