## Markdown extension (e.g. md, markdown, mdown).
MEXT = mdown

## All markdown files in the working directory
SRC = $(wildcard *.$(MEXT))

## Location of Pandoc support files.
PREFIX = /Users/nick/.pandoc/pandoc-templates

## Location of your working bibliography file
MENDELEY_BIB = /Users/nick/school/iSchool/references/library.bib 
## library.bib is a huge, full collection library; probably better to replace this with a Mendeley collection just for this paper 

BIB = library.bib

## CSL stylesheet (located in the csl folder of the PREFIX directory).
CSL = apsa

## ieee-with-url-npd, for submission to IEEE events


PDFS=$(SRC:.mdown=.pdf)
HTML=$(SRC:.mdown=.html)
TEX=$(SRC:.mdown=.tex)


all:	$(PDFS) $(HTML)

pdf:	clean $(PDFS)
html:	clean $(HTML)
tex:	clean $(TEX)


%.html:	%.mdown
	PYTHONPATH=/Users/nick/code/citeproc/citeproc-py/ pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block+link_attributes -t html5 -S -N --template=$(PREFIX)/templates/html.template -V lang=en --section-divs --css=style.css --include-in-header header.include --filter ./cite-filter.py --filter ./svg-pdf-filter.py --csl=$(PREFIX)/csl/$(CSL).csl -o $@ $<

%.tex:	%.mdown
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w latex -s -S -N --latex-engine=pdflatex --template=$(PREFIX)/templates/latex.template --filter pandoc-citeproc --filter ./svg-pdf-filter.py --csl=$(PREFIX)/csl/$(CSL).csl -o $@ $<

%.pdf:	%.mdown
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block -w latex -s -S -N --latex-engine=pdflatex --template=$(PREFIX)/templates/latex.template --filter ./svg-pdf-filter.py --filter pandoc-citeproc --csl=$(PREFIX)/csl/$(CSL).csl -o $*.pdf $<
	
	## if you need to do processing between .tex and .pdf, change the above line to output .tex and uncomment the lines below as necessary
	##./replace.sh
	##pdflatex $*.tex
	##rm *.aux
	##rm *.log
	##rm *.out
	##rm *.tex.bak
	

references:
	cp $(MENDELEY_BIB) $(BIB)
	biber $(BIB) --tool biber.conf
	mv library_bibertool.bib $(BIB)

clean:
	rm -f *.html *.pdf *.tex
	rm -f *.aux *.bcf *.out *.log *.run.xml *.blg
	rm library_bibertool.bib