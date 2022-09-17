FROM python:3.10.7   as build
RUN pip install -g pdm
WORKDIR /build/
COPY ./ ./
RUN pdm install -G dj-raspberrypi \
    && pdm export -f setuppy -o setup.py \
    && pip install -r requirements.txt \
    && python setup.py bdist_wheel \
    && mv requirements.txt dist/

FROM python:3.10.7-slim
WORKDIR /tmp
COPY --from=build /build/dist/*.whl ./
RUN pip install -r requirements.txt && pip install x007007007_respberrypi-0.1.0-py3-none-any.whl

CMD []