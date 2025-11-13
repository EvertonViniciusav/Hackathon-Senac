-- Criação do banco de dados
CREATE DATABASE hackathon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hackathon;

-- ======================
-- Tabela de Usuários
-- ======================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('master', 'usuario') DEFAULT 'usuario',
    is_master BOOLEAN DEFAULT FALSE
);

-- ======================
-- Tabela de Frotas
-- ======================
CREATE TABLE frotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo ENUM('moto', 'carro', 'caminhao', 'aviao', 'trem', 'embarcacao') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ======================
-- Tabela de Documentos
-- ======================
CREATE TABLE documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    frota_id INT NOT NULL,
    tipo_documento VARCHAR(255) NOT NULL,
    data_vencimento DATE NOT NULL,
    FOREIGN KEY (frota_id) REFERENCES frotas(id) ON DELETE CASCADE
);

-- ======================
-- Inserir Usuário Master (Administrador principal)
-- ======================
INSERT INTO usuarios (nome, email, senha, is_master)
VALUES ('Administrador Master', 'master@master.com', 'scrypt:32768:8:1$1zd8d7tUI0ilUIL0$c828d7c5859aa3721533fdfdc2bb3b9fd7c356b16eb98688fa21382c39c18428379c1028e6c78fffb870c52550b55f6513fb57da397f387829179997ffd45f27', TRUE);

-- usuario: master@master.com
-- senhas: master