#!/usr/bin/env python

"""
Pandoc filter to citeproc-py.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from citeproc.py2compat import *
import sys
import functools

# The references are parsed from a BibTeX database, so we import the
# corresponding parser.
from citeproc.source.bibtex import BibTeX

# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem

from pandocfilters import walk, RawInline, RawBlock, Cite, Span, Str, Para, Div, attributes
import json
import logging

def citation_register(key, value, format, meta):
    if key == 'Cite':
        citation = Citation([CitationItem(value[0][0]['citationId'])])
        bibliography.register(citation)
        citations.append(citation)

def citation_replace(key, value, format, meta):
    if key == 'Cite':
        global counter
        citation = citations[counter]
        counter = counter + 1
        bib_citation = bibliography.cite(citation, logging.warn)
        if isinstance(bib_citation, basestring):
          rendered_citation = render(bib_citation)
        else:
          rendered_citation = render(''.join(bib_citation)) # important if there's an "et al.", for example
        return Cite(value[0], [rendered_citation])

def value_of_metadata(result):
    result_value = result['c']
    
    if isinstance(result_value, basestring):    # sometimes the value is a string (if passed as cli argument)
        return result_value
    else:
        return result_value[0]['c']     # other times it's a string inside an array (if in YAML)

if __name__ == "__main__":
    # follows the basic model of pandocfilters toJSONFilter, but we do multiple passes
    doc = json.loads(sys.stdin.read())
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""
    
    if format in ['html', 'html5']:
        f = formatter.html
        render = functools.partial(RawInline, 'html')
    elif format == 'rst':
        f = formatter.rst
        render = Str
    else:
        f = formatter.plain
        render = Str
    
    citations = []
    counter = 0
    bibliography_path = None
    csl_path = None
    
    meta = doc[0]['unMeta']
    
    result = meta.get('bibliography', {})
    if result:
        bibliography_path = value_of_metadata(result)
    result = meta.get('csl', {})
    if result:
        csl_path = value_of_metadata(result)
    
    if bibliography_path == None or csl_path == None:
        raise Exception('Metadata variables must be set for both bibliography and csl.')
    
    # Parse the BibTeX database.
    bib_source = BibTeX(bibliography_path, encoding='utf-8')

    # load a CSL style
    bib_style = CitationStylesStyle(csl_path, validate=False)
    
    bibliography = CitationStylesBibliography(bib_style, bib_source, f)
        
    altered = walk(doc, citation_register, format, doc[0]['unMeta'])
    second = walk(altered, citation_replace, format, doc[0]['unMeta'])
    
    references = []
    for item, key in zip(bibliography.bibliography(), bibliography.keys):
        attrs = {'id': key, 'class':'h-cite'}
        references.append(Div(attributes(attrs),[Para([render(str(item))])]))
        
    second[1].extend(references) # add more paragraphs to the end of the main document list of blocks
    
    json.dump(second, sys.stdout)