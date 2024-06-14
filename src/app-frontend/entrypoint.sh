#!/bin/sh

# Set the default environment to production if not provided
API_URL=${API_URL:-http://localhost:8081}

# Replace the environment variable in the JS file
sed -i "s|{{API_URL}}|$API_URL|g" /usr/share/nginx/html/script.js


# Start nginx
exec nginx -g 'daemon off;'
