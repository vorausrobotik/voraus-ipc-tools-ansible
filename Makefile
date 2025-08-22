GALAXY_IN := voraus/ipc_tools/galaxy.in.yml
GALAXY_OUT := voraus/ipc_tools/galaxy.yml

.PHONY: clean build

build:	version
	ansible-galaxy collection build voraus/ipc_tools

version: clean
	# Replace dev suffixes with rc identifier(e.g. 0.1.dev62+g27abb0f -> 0.1-rc.62)
	@GIT_TAG=$$(python -m setuptools_scm -f plain | sed -E 's/\.dev([0-9]+)\+g[0-9a-f]+/-rc.\1/' 2>/dev/null); \
	if [ $$? -ne 0 ]; then \
		echo "Error: Failed to retrieve git tag using setuptools_scm"; \
		exit 1; \
	fi; \
	echo "Generating $(GALAXY_OUT) with version $$GIT_TAG"; \
	sed "s/__VERSION__/$$GIT_TAG/" $(GALAXY_IN) > $(GALAXY_OUT)

clean:
	@rm -f $(GALAXY_OUT)
	@rm -f *.tar.gz
