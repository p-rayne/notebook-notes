# notebook-notes
application for saving private user notes

docker-compose.yml - запускает Django и Postgres. 

При запуске база данных будет очищена, 
будут выполнены миграции.(файл notebook/entrypoint.sh)

Для запуска контейнера с приложением используйте:
docker-compose up -d --build

