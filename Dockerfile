FROM oven/bun:alpine AS builder

ENV PATH="/root/.bun/bin:${PATH}"
WORKDIR /usr/src/app
COPY package.json tsconfig.json bun.lockb* ./
RUN bun install
COPY src ./src
RUN bun run build


FROM oven/bun:alpine

ENV PATH="/root/.bun/bin:${PATH}"
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/package.json ./package.json
RUN bun install --production --ignore-scripts
EXPOSE 3001

RUN addgroup -S scout && adduser -S appuser -G scout
RUN chown -R appuser:scout /usr/src/app/
USER appuser

CMD ["bun", "run", "dist/src/server/express.js"]
