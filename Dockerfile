# ===========================================================================
#  Multi-stage Dockerfile — smaller, more secure final image.
#  Stage 1 ("builder") installs dependencies with all the build machinery.
#  Stage 2 (final) copies ONLY the installed packages + app code into a
#  clean, minimal image — leaving pip caches and build tools behind.
# ===========================================================================

# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies into a separate folder we can copy out cleanly.
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: final (slim) image ----------
FROM python:3.11-slim

WORKDIR /app

# Copy ONLY the installed Python packages from the builder stage.
COPY --from=builder /install /usr/local

# Copy just the application code (not build junk).
COPY app.py .

# Run as a non-root user for better security (also a nice interview point).
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
