FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and content assets used by the server
COPY src/ src/
COPY spec/ spec/
COPY prompts/ prompts/
COPY tool_specs/ tool_specs/
COPY templates/ templates/

# Expose the port
EXPOSE 8100

# Run the server
# Use python directly as server.py has the uvicorn.run block
CMD ["python", "src/server.py"]
