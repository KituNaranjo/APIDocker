FROM ubuntu

# Actualizar el sistema e instalar las dependencias necesarias
RUN apt-get update 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY app.py .
COPY requirements.txt .

# Instalar las dependencias del proyecto
RUN pip3 install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que la aplicación estará escuchando
EXPOSE 8000

# Comando para ejecutar la aplicación
#CMD ["python3", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
