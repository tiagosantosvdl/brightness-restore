.PHONY: release _build

# Stage and package the extension without installing into the running session.
_build:
	node .scripts/validate-build.js
	rm -rf _build
	mkdir -p _build
	cp -r extension/. _build/
	cp LICENSE _build/
	glib-compile-schemas --strict _build/schemas

release: _build
	python3 scripts/package-release.py --build-dir _build
