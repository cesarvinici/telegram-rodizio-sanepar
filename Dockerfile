FROM python:3

WORKDIR /app

COPY requirements.txt .
COPY ./data ./data

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/core.py"]