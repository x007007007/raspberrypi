FROM python:3.10.7   as build
RUN pip install pdm && pip install -U 'setuptools<=57.4'
WORKDIR /build/
COPY ./pyproject.toml ./
RUN pdm install -dG:all -G:all
COPY ./ ./
RUN pdm install -dG:all -G dj-raspberrypi \
    && pdm export -f setuppy -o setup.py \
    && pdm export -f requirements -o requirements.txt \
    && python setup.py bdist_wheel \
    && mv requirements.txt dist/

FROM python:3.10.7-slim
WORKDIR /tmp
COPY --from=build /build/dist/* ./
RUN pip install x007007007_respberrypi-0.1.0-py3-none-any.whl

CMD []