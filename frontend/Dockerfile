# Build stage
FROM node:16-alpine as build

# Install pnpm
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy the root package.json, pnpm-lock.yaml, and pnpm-workspace.yaml
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy the frontend package.json
COPY frontend/package.json ./frontend/

# List contents of current directory for debugging
RUN ls -la

# Install dependencies with verbose output
RUN pnpm install --no-frozen-lockfile --verbose

# Copy the rest of the application code
COPY . .

# List contents of frontend directory for debugging
RUN ls -la frontend

# Build the frontend application
WORKDIR /app/frontend
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy the build output to replace the default nginx contents
COPY --from=build /app/frontend/dist /usr/share/nginx/html

# Expose port 3000
EXPOSE 3000

# Copy the custom nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]