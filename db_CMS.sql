
CREATE TABLE IF NOT EXISTS autores(
    autor_id SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    apellido VARCHAR(25) NOT NULL,
    seudonimo VARCHAR(50) UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    pais_origen VARCHAR(40),
    fecha_creacion DATE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS categorias(
    categoria_id SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(25) NOT NULL,
    descripcion VARCHAR(250) NOT NULL,
    fecha_creacion DATE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS articulos(
    articulo_id SERIAL PRIMARY KEY,
    autor_id INT NOT NULL,
    categoria_id INT NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    contenido TEXT,
    fecha_publicacion DATE NOT NULL,
    fecha_ultima_actualizacion DATE DEFAULT NOW(),
    fecha_creacion DATE DEFAULT NOW(),
    CONSTRAINT fk_autor
        FOREIGN KEY (autor_id) REFERENCES autores(autor_id) ON DELETE CASCADE,
        FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE CASCADE
);

INSERT INTO autores(nombre, apellido, seudonimo, fecha_nacimiento, pais_origen)
VALUES ('Antoine','Saint-Exupéry','anton','1900-06-29','Francia');


INSERT INTO categorias(nombre_categoria, descripcion)
VALUES('infantil','cuentos, historias adecuadas para infantes de entre 5 y 10 años');

INSERT INTO articulos(autor_id, categoria_id, titulo,contenido, fecha_publicacion)
VALUES (1,1,'El Principito','El principito (en francés: Le Petit Prince) es una novela corta y la obra más famosa del escritor y aviador francés Antoine de Saint-Exupéry (1900-1944)','1943-04-06');