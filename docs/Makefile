# Minimal makefile for MkDocs documentation
#

# You can set these variables from the command line
MKDOCS ?= mkdocs
SOURCEDIR = .
BUILDDIR = site

# Put it first so that "make" without argument is like "make help"
help:
	@echo "MkDocs documentation build commands:"
	@echo "  serve    Start development server"
	@echo "  build    Build the documentation"
	@echo "  clean    Clean the build directory"
	@echo "  deploy   Deploy to GitHub Pages"

.PHONY: help serve build clean deploy

serve:
	@$(MKDOCS) serve

build:
	@$(MKDOCS) build

clean:
	@rm -rf "$(BUILDDIR)"

deploy:
	@$(MKDOCS) gh-deploy