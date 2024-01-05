FROM postgres:latest

# Configurar usuario y contraseña (modificar según sea necesario)
ENV POSTGRES_USER=grupodos
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=mydatabase

# Puerto expuesto (modificar según sea necesario)
EXPOSE 5432

# Volumen para persistencia de datos
VOLUME /var/lib/postgresql/data

# Cambiar al directorio /docker-entrypoint-initdb.d para la inicialización de la base de datos
WORKDIR /docker-entrypoint-initdb.d

# Copiar scripts SQL de inicialización (si es necesario)
COPY init.sql .

# Comando para ejecutar la base de datos
CMD ["postgres"]
