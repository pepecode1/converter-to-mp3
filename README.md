## Aplicación web para descargar videos de YouTube o pistas de SoundCloud y convertirlas a MP3.

## Requisitos
- Python 3.x
- Dependencias: `flask`, `yt-dlp`, `pydub`
- FFmpeg instalado

## Uso
- Abre http://127.0.0.1:5000/ en tu navegador.
- Pega un enlace de YouTube (por ejemplo, https://www.youtube.com/watch?v=VIDEO_ID) o SoundCloud (por ejemplo, https://soundcloud.com/artist/track-name).
- Haz clic en "Descargar MP3" para obtener el archivo.

## Términos de uso
- Uso legal: Esta aplicación está destinada únicamente para descargar contenido que tengas permiso para usar. Debes cumplir con los términos de servicio de YouTube y SoundCloud, así como con las leyes de derechos de autor aplicables en tu país.
- Restricciones: Solo se pueden descargar pistas de SoundCloud habilitadas para descarga por el artista. Algunos videos de YouTube pueden estar restringidos por región o requerir autenticación.
- Responsabilidad: El usuario es el único responsable del uso de esta aplicación. Los desarrolladores no se hacen responsables por el mal uso o violaciones de derechos de autor.

## Licencia
- Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.NotasLos archivos descargados se almacenan temporalmente en static/downloads. Considera eliminarlos periódicamente para liberar espacio.
- Esta es una aplicación de demostración. Para uso en producción, implementa medidas de seguridad adicionales y limpieza automática de archivos.
- Si tienes problemas con descargas de SoundCloud, verifica que la pista esté habilitada para descarga en la plataforma.

## Contribuciones
- ¡Las contribuciones son bienvenidas! Por favor, abre un issue o un pull request en el repositorio para sugerencias o mejoras.

