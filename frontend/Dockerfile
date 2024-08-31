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

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

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