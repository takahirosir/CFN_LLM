FROM python:3.10
WORKDIR /CFN_LLM
COPY requirement.txt .
RUN pip install -r requirement.txt
