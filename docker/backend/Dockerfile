FROM python:3.9-slim

WORKDIR /cf-backend-container
RUN apt-get update && \
    apt-get install -y  default-libmysqlclient-dev gcc g++ \
    && apt-get install -y ffmpeg libsm6 libxext6 ninja-build libglib2.0-0 libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

COPY ./cf-backend/requirements.txt ./requirements.txt

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install openmim \
    && mim install "mmengine>=0.6.0" \
    && mim install "mmcv>=2.0.0rc4,<2.1.0" \
    && mim install "mmdet>=3.0.0rc6,<3.1.0" \
    && mim install "mmocr>=1.0.0rc0" \
    && mim install "mmyolo" \
    && rm -rf /root/.cache/pip

COPY ./cf-backend/ .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
CMD ["daphne","-b","0.0.0.0","-p","8000","apiproject.asgi:application"]






