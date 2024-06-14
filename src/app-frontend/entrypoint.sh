#!/bin/sh

# Set the default environment to production if not provided
API_URL=${API_URL:-http://localhost:8081}

ENVIRONMENT=${ENVIRONMENT:-standard}

case "$ENVIRONMENT" in
  standard)
    cp /usr/share/nginx/html/index.standard.html /usr/share/nginx/html/index.html
    cp /usr/share/nginx/html/script.standard.js /usr/share/nginx/html/script.js
    ;;
  colorfull)
    cp /usr/share/nginx/html/index.colorfull.html /usr/share/nginx/html/index.html
    cp /usr/share/nginx/html/script.colorfull.js /usr/share/nginx/html/script.js
    ;;
  *)
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

# Replace the environment variable in the JS file
sed -i "s|{{API_URL}}|$API_URL|g" /usr/share/nginx/html/script.js


# Start nginx
exec nginx -g 'daemon off;'
