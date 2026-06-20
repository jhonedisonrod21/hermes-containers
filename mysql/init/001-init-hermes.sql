-- Bases de datos por contexto acotado (bounded context). Idempotente.
-- El usuario de aplicación lo crea el entrypoint a partir de MYSQL_USER/MYSQL_PASSWORD;
-- aquí solo se crean las bases restantes y se otorgan privilegios.
--
--   HERMES_IAM       -> auth-server, identity-service, tenant-service
--   HERMES_CALENDAR  -> catalog-service, scheduling-service, integration-hub-service
--   HERMES_COMMERCE  -> payment-service, notification-service

CREATE DATABASE IF NOT EXISTS `HERMES_IAM`      CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `HERMES_CALENDAR` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `HERMES_COMMERCE` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON `HERMES_IAM`.*      TO 'hermes_app'@'%';
GRANT ALL PRIVILEGES ON `HERMES_CALENDAR`.* TO 'hermes_app'@'%';
GRANT ALL PRIVILEGES ON `HERMES_COMMERCE`.* TO 'hermes_app'@'%';
FLUSH PRIVILEGES;
