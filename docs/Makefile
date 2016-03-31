OBJECT = proposal
LATEX = latex
BIBTEX = bibtex

DEFAULT:
	make $(OBJECT).pdf

$(OBJECT).dvi: Makefile $(SOURCES)
	$(LATEX)  $(OBJECT)
	$(BIBTEX) $(OBJECT)
	$(LATEX)  $(OBJECT)
	$(LATEX)  $(OBJECT)

$(OBJECT).ps: $(OBJECT).dvi
	dvips $(OBJECT)

$(OBJECT).pdf: $(OBJECT).ps
	ps2pdf $(OBJECT).ps
	
evince: $(OBJECT).pdf
	evince $(OBJECT).pdf

view: $(OBJECT).pdf
	acroread $(OBJECT).pdf
	
clean:
	rm -f *.aux  *.nav *.out *.snm *.toc *.blg *.end *.log *~ *.nlo *.ist *.nls *.tmp sections/*.aux sections/*.tmp

cleaner:
	rm -f *.bbl *.dvi *.ps *.aux  *.nav *.out *.snm *.toc *.blg *.end *.log *~ *.nlo *.ist *.nls *.tmp sections/*.aux sections/*.tmp
	
pristine:
	make clean
	rm -f *.bbl $(OBJECT).pdf $(OBJECT).ps $(OBJECT).dvi
