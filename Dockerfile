FROM python:3.9-slim

COPY requirements.txt /tmp/requirements.txt
COPY README.md /tmp/README.md
COPY setup.py /tmp/setup.py
COPY redbox /tmp/redbox

RUN set -eux \
	&& cd /tmp \
	&& python setup.py install

ENTRYPOINT ["/usr/local/bin/redbox_exporter"]
