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

app.listen(PORT, async () => {
  logger.info(`Server running on port ${PORT}`);
  await handshake().catch((err) => {
    logger.error(err.message);
    process.exit(1);
  });
});

export default app;
