FROM python:3.9-slim
WORKDIR /app
# Install only what is needed for prediction
RUN pip install flask pandas scikit-learn
COPY fraud_api.py .
COPY fraud_model.pkl . 
EXPOSE 5001
CMD ["python", "fraud_api.py"]
