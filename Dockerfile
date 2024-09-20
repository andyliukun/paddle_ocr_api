FROM python:3.10.9

# 设置工作目录，即cd命令
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY server.py ./server.py

EXPOSE 8000

# 镜像运行时执行的命令，这里的配置等于 EXPOS server.app
CMD ["sanic","server.app","--host=0.0.0.0","--port=8000"]
