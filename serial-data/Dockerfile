FROM python:3.8.2


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY daq.py ./daq.py

CMD ["uvicorn", "daq:app", "--host", "0.0.0.0", "--port", "80"]
