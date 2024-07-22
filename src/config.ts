import "dotenv/config";

import { cleanEnv, json, makeValidator, num, port, str, url } from "envalid";

import { LLMProvider } from "./utils/llm";

process.env.OPENAI_API_KEY = process.env.OPENAI_API_KEY || "";
process.env.OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY || "";

// Validator for LLM providers
const providersValidator = makeValidator((x) => {
  const providers = x.split(",") as LLMProvider[];
  if (providers.length === 0) {
    throw new Error("No PROVIDERS provided");
  }
  providers.forEach((provider) => {
    if (!Object.values(LLMProvider).includes(provider)) {
      throw new Error(`Invalid PROVIDER: ${provider}`);
    }
  });

  return providers;
});

// Validator for API keys based on provider type
const apiKeyValidator = (type: string, providers: LLMProvider[]) =>
  makeValidator((apiKey) => {
    // If the provider is not in the list, we don't need to validate the API key
    if (!providers.includes(type as LLMProvider)) {
      return apiKey;
    }

    switch (type) {
      case "groq": {
        if (!apiKey.startsWith("gsk_")) {
          throw new Error(`Invalid ${type} API key: ${apiKey}`);
        }
        break;
      }
      case "openai":
      case "openrouter": {
        if (!apiKey.startsWith("sk")) {
          throw new Error(`Invalid ${type} API key: ${apiKey}`);
        }
        break;
      }
      case "chasm": {
        if (apiKey.length !== 44) {
          throw new Error(`Invalid ${type} API key: ${apiKey}`);
        }
        break;
      }
      default: {
        throw new Error(`Invalid API key type: ${type}`);
      }
    }

    return apiKey.trim();
  });

const PROVIDERS = process.env.PROVIDERS?.split(",") as LLMProvider[];
const handshakeProtocol = process.env.NODE_ENV !== "local" ? "wss" : "ws";

// Validate and clean environment variables
export const env = cleanEnv(process.env, {
  PORT: port({
    default: 3001,
  }),
  LOGGER_LEVEL: str({ choices: ["debug", "info", "warn", "error", "fatal"] }),
  ORCHESTRATOR_URL: url(),
  SCOUT_NAME: str(),
  SCOUT_UID: num(),
  WEBHOOK_API_KEY: str(),
  WEBHOOK_URL: url(),
  PROVIDERS: providersValidator(),
  GROQ_API_KEY: apiKeyValidator("groq", PROVIDERS)(),
  OPENAI_API_KEY: apiKeyValidator("openai", PROVIDERS)(),
  OPENROUTER_API_KEY: apiKeyValidator("openrouter", PROVIDERS)(),
  MODEL: str(),
  OPENROUTER_CUSTOM_CONFIG: json({
    default: {
      temperature: 0,
      provider: {
        allow_fallbacks: false,
        order: ["Fireworks"],
      },
    },
  }),

  // Optional
  HANDSHAKE_PROTOCOL: str({
    choices: ["ws", "wss"],
    default: handshakeProtocol,
  }),
  IP: str({ default: "127.0.0.1" }),
});
