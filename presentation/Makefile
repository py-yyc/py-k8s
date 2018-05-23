RUBBER_INFO = rubber-info
RUBBER = rubber --unsafe -m graphics -m xelatex --warn=refs --warn=misc
.SECONDARY:
SHELL = /bin/bash -eu

-include Makefile.local

all: annotated-presentation-skim.pdf presentation-skim.pdf

skim: annotated-presentation-skim.pdf
	open -a /Applications/Skim.app $<

annotated-presentation.pdf: presentation.tex

.PHONY: .FORCE

annotated-presentation.pdf: labels.aux

labels.aux: presentation-skim.pdf
	grep '^\\newlabel' presentation.aux > $@ ||:

%.pdf: %.tex .FORCE
	#iconv -f UTF-8 -t US-ASCII $< > /dev/null
	${RUBBER} $<
	if grep -q 'fourupslides Warning: $*-skim.pdf not found' $*.log; then \
	    cat $@ > $*-skim.pdf; \
	    ${RUBBER} --force $<; \
	fi
	$(EXTRA_CMDS)

%-skim.pdf: %.pdf
	cat $< > $@

clean::
	rm -f *.aux *.log *.snm *.toc *.nav *.out *.toc *.vrb \
	    {annotated-,}presentation*.pdf \
	    transcript.tex transcript*.pdf

realclean:: clean
	rm -f {annotated-,}presentation-skim.pdf

PYTHON_FILES = $(wildcard *.py)

presentation.pdf: $(PYTHON_FILES:%.py=%.py.include)

clean::
	rm -f *.out *.include

GH_CURL = curl -sSH "Authorization: token $$(grep oauth_token ~/.config/hub  | head -n1 | awk '{print $$2}')"

upload: presentation.pdf
	git tag -f v0.0.0 && git push -f --tags github.com/py-yyc/py-k8s
	EXISTING_RELEASE_ID=$$(${GH_CURL} https://api.github.com/repos/py-yyc/py-k8s/releases/tags/v0.0.0 | jq .id); \
	if [ -n "$$EXISTING_RELEASE_ID" ]; then \
	    ${GH_CURL} -X DELETE https://api.github.com/repos/py-yyc/py-k8s/releases/$$EXISTING_RELEASE_ID; \
	fi
	hub release create -p -a presentation.pdf -m Slides v0.0.0

