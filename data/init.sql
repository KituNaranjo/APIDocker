CREATE TABLE tareas (id SERIAL PRIMARY KEY, nombre VARCHAR(255), tarea VARCHAR(255) NOT NULL);

INSERT INTO tareas (nombre, tarea) VALUES ('Christian', 'Conexion Backend con Frontend');
INSERT INTO tareas (nombre, tarea) VALUES ('Leandro', 'Revisar el Frontend');
INSERT INTO tareas (nombre, tarea) VALUES ('Sara', 'Diseño del Frontend');
INSERT INTO tareas (nombre, tarea) VALUES ('Bryan', 'Database');
