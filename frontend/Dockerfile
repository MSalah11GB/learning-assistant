FROM node:20-alpine AS base

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# NEXT_PUBLIC_* vars are inlined into the client bundle at build time, so this
# must be passed as a build arg — env_file/environment in docker-compose only
# apply at container runtime, too late for `next build`.
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
