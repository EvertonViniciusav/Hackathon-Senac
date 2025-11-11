CREATE DATABASE hackathon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hackathon;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(120) UNIQUE,
    senha VARCHAR(255)
);

CREATE TABLE frotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nome VARCHAR(100),
    tipo ENUM('moto', 'carro', 'caminhao', 'aviao', 'trem'),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    frota_id INT,
    tipo_documento VARCHAR(255),
    data_vencimento DATE,
    FOREIGN KEY (frota_id) REFERENCES frotas(id) ON DELETE CASCADE
);
