# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Cloud Run uses 8080)
EXPOSE 8080

# Run Streamlit
CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0