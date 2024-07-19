# Updating Scout

## Pull the latest code

```sh
# Pull the latest code
git fetch
git pull origin main
```

## Docker container

### For Docker Run

```sh
# Restart docker
docker stop scout
docker rm scout

# Rebuild docker
docker build --tag 'chasm_scout' .
# Can consider adding --restart=always flag to always restart for production
docker run --env-file ./.env -p 3001:3001 --name scout chasm_scout
```

### For Docker Compose

```sh
docker compose down
PORT=3001 docker-compose up --build -d
```
