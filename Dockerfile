FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install streamlit langchain langgraph langchain-groq python-dotenv

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]