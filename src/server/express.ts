import chalk from "chalk";
import express from "express";

import { env } from "../config";
import { apikeyAuthMiddleware } from "../middleware/apiKeyMiddleware";
import { logger } from "../utils/logger";
import { handshake } from "./handshake";
import { webhook } from "./webhook";

const {
  GROQ_API_KEY,
  OPENAI_API_KEY,
  OPENROUTER_API_KEY,
  ORCHESTRATOR_URL,
  PORT,
  PROVIDERS,
  SCOUT_NAME,
  SCOUT_UID,
} = env;

function getProviders() {
  const providers = [];
  if (OPENAI_API_KEY) {
    providers.push("OpenAi");
  }
  if (GROQ_API_KEY) {
    providers.push("Groq");
  }
  if (OPENROUTER_API_KEY) {
    providers.push("OpenRouter");
  }
  return providers.join(", ");
}

logger.info(`Starting Scout ⚜️`);
logger.info("--------------------------------------------");
logger.info(`Scout UID: ${chalk.bold(SCOUT_UID)}`);
logger.info(`Scout Name: ${chalk.bold(SCOUT_NAME)}`);
logger.info(`Port: ${chalk.bold(PORT)}`);
logger.info(`Providers: ${chalk.bold(PROVIDERS.join(", "))}`);
logger.info(`Provider API Key set for: ${chalk.bold(getProviders())}`);
logger.info(`Orchestrator URL: ${chalk.bold(ORCHESTRATOR_URL)}`);
logger.info("--------------------------------------------");

const app = express();

app.use(express.json());

// app.post("/", webhook);
app.post("/", apikeyAuthMiddleware, webhook());
app.post("/v1/chat/completions", apikeyAuthMiddleware, webhook(true));
app.get("/", (req, res) => {
  return res.status(200).send("OK");
});

async function retryWithExponentialBackoff(
  retries: number,
  fn: () => Promise<unknown>,
): Promise<void> {
  const initialDelay = 1000; // 1s start
  let delayFactor = 30; // Initial growth factor

  let previousDelay = initialDelay;
  const delays = [initialDelay];

  for (let attempt = 1; attempt < retries; attempt++) {
    let currentDelay = previousDelay * delayFactor;

    while (currentDelay <= previousDelay) {
      delayFactor += 0.5;
      currentDelay = previousDelay * delayFactor;
    }

    // 30 mins cap
    if (currentDelay > 30 * 60 * 1000) {
      currentDelay = 30 * 60 * 1000;
    }

    delays.push(currentDelay);
    previousDelay = currentDelay;
  }

  logger.info(`Delays: ${delays.map((d) => d / 1000).join(", ")} seconds`);

  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      await fn();
      return;
    } catch (err: any) {
      logger.error(`Attempt ${attempt + 1} failed: ${err.message}`);
      if (attempt < retries - 1) {
        const delay = delays[attempt];
        logger.info(`Retrying in ${delay / 1000} seconds...`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      } else {
        logger.error("All retry attempts failed. Exiting gracefully.");
        process.exit(1);
      }
    }
  }
}

app.listen(PORT, async () => {
  logger.info(`Server running on port ${PORT}`);
  logger.info("Running exponential backoff handshake...");
  await retryWithExponentialBackoff(6, handshake);
});

export default app;
