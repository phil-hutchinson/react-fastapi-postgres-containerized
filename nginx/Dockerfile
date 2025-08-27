FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy dashboard.html to be served by nginx
COPY dashboard.html /usr/share/nginx/html/dashboard.html

# Create index.html that redirects to dashboard.html
RUN echo '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=/dashboard.html"></head><body>Redirecting...</body></html>' > /usr/share/nginx/html/index.html

EXPOSE 80
