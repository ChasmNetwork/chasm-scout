# Setup Guide

## Prerequisite

- Server Requirement

  - Operating System: Linux (linux/amd64, linux/arm64)
  - Min Requirement: 1 vCPU, 1GB RAM / 20GB Disk, Static IP
  - Suggested Requirement: 2 vCPU, 4GB RAM / 50GB SSD, Static IP

- Docker installation: https://docs.docker.com/engine/install/ubuntu/

# Quick run

0. Getting API Key from API Provider

- [Groq](https://console.groq.com/keys)

1. Prepare a .env file and copy paste it from [.env.sample](../.env.sample) and edit to your own need

```sh
# Use your fav text editor, vim/nano
nano .env
```

2. Pull the docker images from https://hub.docker.com/r/chasmtech/chasm-scout

```sh
docker pull chasmtech/chasm-scout:latest
```

3. Run the file

```sh
docker run -d --restart=always --env-file ./.env -p 3001:3001 --name scout chasmtech/chasm-scout
```

# Run docker from codebase

## 1. Download Codebase

Download the codebase

```sh
# Download Via SSH
git clone git@github.com:ChasmNetwork/chasm-scout.git
# Download Via HTTPS
git clone https://github.com/ChasmNetwork/chasm-scout.git
```

Navigate to the project directory

```
cd chasm-scout
```

## 2. Getting API Key and UID from Chasm

- Follow the steps provided by Chasm Network to obtain your API key and UID.

## 3. Getting API Key from API Provider

- [OpenAI ChatGPT API](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
- [Groq](https://console.groq.com/keys)

## 4. Setup .env

To the run command below replacing the path to your `.env` file

```bash
# Copy dot env
cp .env.sample .env
```

Update the `.env` file

## 5. Running the server with Docker

> Scouts need to establish an internet connection with the orchestrator. This requires ensuring that the `PORT` specified in .env is reachable on the Docker Container via the internet. This involves either opening the port on the firewall or configuring port forwarding.

```bash
# Build Docker Image
docker build --tag 'chasm_scout' .
# Run docker
# Can consider adding --restart=always flag to always restart for production
# Note: Remember to change the port
docker run --env-file ./.env -p 3001:3001 --name scout chasm_scout
```

Alternative: Docker Compose

```
PORT=3001 docker compose up -d
```

## 6. Verifying the Setup

Access the running application at http://<your-server-ip>:3001 to verify the setup.

Check the Docker container logs for any issues:

```bash
docker logs scout
```

# Run via Nodejs

Make sure your node.js version are >21 and have bun installed

```sh
bun i
bun run build
bun run dist/server/express.js
```

## Troubleshooting

- **Environment Variables**: Double-check that all required environment variables are set correctly in the `.env` file.

## Additional Resources

- **Optimization Guide**: Follow the [optimization guide](/docs/OPTIMZATION.md) for performance improvements.
- **Update Guide**: Follow the [update guide](/docs/UPDATE.md) for updating your scout.
