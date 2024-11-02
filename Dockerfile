# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /FLASK_CHALLENGE_FINAL

# Copiar los archivos de requisitos y el código fuente
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que corre tu aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]