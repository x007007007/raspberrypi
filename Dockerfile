FROM python:3.10.7 as rust_build
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        curl \
    && curl https://sh.rustup.rs -sSf | bash -s -- -y \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --upgrade pip \
    && pip install pdm \
    && pdm config python.use_venv false \
    && pip install setuptools-rust


FROM rust_build as cryptography_build
RUN . "$HOME/.cargo/env" \
    && rustup --version \
    && pip download cryptography==38.0.1 \
    && tar -xzvf cryptography-38.0.1.tar.gz \
    && cd cryptography-38.0.1 \
    && python setup.py bdist_wheel

FROM rust_build as build
WORKDIR /build/
COPY --from=cryptography_build  /cryptography-38.0.1/dist/ ./dist/
COPY ./pyproject.toml ./
RUN . "$HOME/.cargo/env" \
    && pip install ./dist/*.whl \
    && pdm install -dG:all -G:all
COPY ./ ./
RUN . "$HOME/.cargo/env" \
    && pdm export -f setuppy -o setup.py \
    && pdm export -f requirements -o requirements.txt \
    && python setup.py bdist_wheel \
    && mv requirements.txt dist/
COPY --from=cryptography_build  /cryptography-38.0.1/dist/ ./dist/


FROM python:3.10.7-slim
WORKDIR /tmp
COPY --from=build /build/dist/* ./
RUN pip install ./cryptography-38.0.1-cp310-cp310-linux_armv7l.whl \
    && pip install ./x007007007_respberrypi-0.1.0-py3-none-any.whl

CMD []