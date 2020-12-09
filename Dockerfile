FROM python

WORKDIR /probe
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD src .
VOLUME [ "/probe/config" ]