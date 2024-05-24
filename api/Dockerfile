# Usa la imagen oficial de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos en el contenedor
COPY requirements.txt .

# Instala los paquetes de Python necesarios
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación en el contenedor
COPY . .

# Expon el puerto en el que escucha tu aplicación Flask
EXPOSE 5000

# Comando para iniciar la aplicación Flask usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
