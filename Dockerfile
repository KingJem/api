# Dockerfile.win
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/whyour/qinglong:python3.10
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && mknod /dev/ptmx c 5 2 \
    && chmod 666 /dev/ptmx \
RUN pip install pyinstaller

WORKDIR /app
VOLUME . .


CMD ["pyinstaller", "-D", "app/main.py", "-i", "app/sync.ico", "--windowed","--clean"]
