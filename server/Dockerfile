FROM python:3.9.7-slim
COPY server /server
COPY server/main.py main.py
RUN python -m unittest server/tests/test_common.py
ENTRYPOINT ["/bin/sh"]
