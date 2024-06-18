CREATE DATABASE psim
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TEMPLATE = template0;

ALTER DATABASE psim SET timezone TO 'Europe/Warsaw';

GRANT ALL PRIVILEGES ON DATABASE psim TO postgres;
