FROM python:3.10.8-alpine3.15

ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

# install runtime dependencies
RUN apk add python3

# runtime dependencies
RUN set -eux; \
    apk add --no-cache \
    ca-certificates \
    tzdata \
    ;

ENV GPG_KEY A035C8C19219BA821ECEA86B64E628F8D684696D
ENV PYTHON_VERSION 3.11.0

ENV PYTHON_PIP_VERSION 22.3

ENV PYTHON_SETUPTOOLS_VERSION 65.5.0

ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/6d265be7a6b5bc4e9c5c07646aee0bf0394be03d/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 36c6f6214694ef64cc70f4127ac0ccec668408a93825359d998fb31d24968d67


RUN set -eux; \
    \
    wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
    echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
    \
    export PYTHONDONTWRITEBYTECODE=1; \
    \
    python3 get-pip.py \
    --disable-pip-version-check \
    --no-cache-dir \
    --no-compile \
    "pip==$PYTHON_PIP_VERSION" \
    "setuptools==$PYTHON_SETUPTOOLS_VERSION" \
    ; \
    rm -f get-pip.py; \
    \
    pip --version

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


