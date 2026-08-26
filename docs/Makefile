SPHINXOPTS ?= --keep-going
SPHINXBUILD ?= sphinx-build
SPHINXAPIDOC ?= sphinx-apidoc
SOURCEDIR = .
BUILDDIR = _build
APIDIR = $(SOURCEDIR)/api
PACKAGEDIR = ../src/torn_sdk
PACKAGEEXCLUDES = $(PACKAGEDIR)/codegen $(PACKAGEDIR)/models $(PACKAGEDIR)/resources/_generated

.PHONY: help clean api html

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf "$(BUILDDIR)"
	rm -rf "$(APIDIR)"

# Recreate the API reference from the SDK source so route changes are always documented.
api:
	rm -rf "$(APIDIR)"
	@$(SPHINXAPIDOC) --force --module-first --separate --output-dir "$(APIDIR)" "$(PACKAGEDIR)" $(PACKAGEEXCLUDES)

html: api
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
