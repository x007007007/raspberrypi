FROM python:3.10.7 as rust_build
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        curl \
    && curl https://sh.rustup.rs -sSf | bash -s -- -y
WORKDIR /build/
RUN pip download cryptography==38.0.1 \
    && pip install -U pip setuptools setuptools-rust \
    && tar -xzvf cryptography-38.0.1.tar.gz \
    && cd cryptography-38.0.1 \
    && python setup.py bdist_wheel

FROM rust_build as build
WORKDIR /build/
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install pdm \
    && pip install -U 'setuptools<=57.4' \
    && pip install setuptools-rust
COPY ./pyproject.toml ./
RUN pdm install -dG:all -G:all
COPY ./ ./
RUN pdm install -dG:all -G dj-raspberrypi \
    && pdm export -f setuppy -o setup.py \
    && pdm export -f requirements -o requirements.txt \
    && python setup.py bdist_wheel \
    && mv requirements.txt dist/
COPY --from=rust_build /build/cryptography-38.0.1/dist/ ./dist/

FROM python:3.10.7-slim
WORKDIR /tmp
COPY --from=build /build/dist/* ./
RUN pip install cryptography*.whl \
    && pip install x007007007_respberrypi-0.1.0-py3-none-any.whl

CMD []