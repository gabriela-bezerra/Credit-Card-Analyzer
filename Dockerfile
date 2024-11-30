FROM python:3.12-slim 

WORKDIR /app 

COPY requirements.txt .


RUN pip install -r requirements.txt


COPY src/ ./src/


EXPOSE 8501 

CMD ["/bin/sh", "-c","cd src && streamlit run app.py --server.address 0.0.0.0"]