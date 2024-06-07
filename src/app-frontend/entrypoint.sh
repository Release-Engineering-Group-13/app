#!/bin/sh

# Set the default environment to production if not provided
ENVIRONMENT=${ENVIRONMENT:-docker}

# Determine the JS file to use based on the environment variable
case "$ENVIRONMENT" in
  docker)
    cp /usr/share/nginx/js/script.docker.js /usr/share/nginx/html/script.js
    ;;
  kubernetes)
    cp /usr/share/nginx/js/script.kubernetes.js /usr/share/nginx/html/script.js
    ;;
  *)
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

# Start nginx
exec nginx -g 'daemon off;'
