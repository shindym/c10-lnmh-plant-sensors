FROM python:latest

WORKDIR /app

COPY requirements.txt .
COPY .streamlit .

RUN pip3 install -r requirements.txt
EXPOSE 8501
COPY app.py .


# When it's all finished, what's the command to start it up?
CMD ["streamlit", "run", "app.py", "--server.port=8501"]