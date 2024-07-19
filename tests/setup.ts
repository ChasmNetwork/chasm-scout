import Chance from "chance";

import "jest-ai";
import "dotenv/config";

// Initialize Chance for generating random data
export const chance: Chance.Chance = new Chance();

// Mock dotenv/config globally
process.env.PORT = "3001";
process.env.LOGGER_LEVEL = "debug";
process.env.ORCHESTRATOR_URL = "http://example.com";
process.env.SCOUT_NAME = "test";
process.env.SCOUT_UID = "123";
process.env.WEBHOOK_API_KEY = "test_api_key";
process.env.WEBHOOK_URL = "http://webhook.example.com";
process.env.PROVIDERS = "groq,openrouter";
process.env.MODEL = "gemma2-9b-it";
