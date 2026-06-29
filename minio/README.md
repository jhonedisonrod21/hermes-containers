# MinIO — almacén de anexos (local)

Almacén de objetos **S3-compatible** para los anexos de tipo `FILE` de las citas. En local
"simula" a Amazon S3: el `scheduling-service` habla S3 contra este contenedor; al desplegar en AWS
solo cambia el `endpoint`/credenciales (config), no el código.

## Uso

```bash
docker compose -f hermes-containers/minio/compose.yml up -d
```

Arranca MinIO y un job efímero (`minio-bootstrap`) que crea el bucket `hermes-requirement-files`
de forma idempotente.

- **API S3:** http://localhost:9100  (la usa el servicio como `hermes.storage.s3.endpoint`)
- **Consola web:** http://localhost:9101  (usuario/clave de `.env`)

## Equivalencia con AWS

| Local (este contenedor)            | AWS                                   |
|------------------------------------|---------------------------------------|
| endpoint `http://localhost:9100`   | endpoint por defecto de S3 (sin override) |
| `MINIO_ROOT_USER` / `_PASSWORD`    | Access key / secret (o rol IAM)       |
| bucket `hermes-requirement-files`  | bucket S3 del mismo nombre            |

El mismo `S3ObjectStorage` del servicio funciona en ambos: con `path-style-access` y el `endpoint`
apuntando aquí en el perfil `local`, y sin `endpoint` (S3 real) en despliegue.
