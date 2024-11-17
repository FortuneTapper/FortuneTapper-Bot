# Usa la imagen oficial de Python
FROM python:3.10

# Instala las dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Instala Playwright y sus navegadores
RUN pip install playwright && playwright install --with-deps

# Copia los archivos del proyecto
COPY . .

# Ejecuta el bot en modo headless
CMD ["python", "bot.py"]