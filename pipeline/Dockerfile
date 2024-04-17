FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements.txt
COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

COPY extract.py .
COPY transform.py .
COPY load.py .
COPY alert.py .
COPY main.py .

CMD [ "main.handler" ]