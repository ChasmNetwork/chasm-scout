#!/bin/sh
# Get the version from package.json
VERSION=$(jq -r '.version' package.json)

# Check if the -y flag is provided
CONFIRM=true
for arg in "$@"
do
    if [ "$arg" = "-y" ]; then
        CONFIRM=false
        break
    fi
done

if $CONFIRM; then
    echo "You are about to build and push the Docker image with version: $VERSION"
    read -p "Do you want to proceed? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborting Docker build and push."
        exit 1
    fi
fi


# Confirm
docker buildx build --platform linux/amd64,linux/arm64 -t johnsonchasm/chasm-scout:$VERSION -t johnsonchasm/chasm-scout:latest --push .
