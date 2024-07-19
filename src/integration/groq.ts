import OpenAI from "openai";

import { env } from "../config";
import { logger } from "../utils/logger";
import { OpenAIBase } from "./OpenAIBase";

class GroqLLM extends OpenAIBase {
  constructor(apiKey: string) {
    // Groq OpenAI Compatibility: https://console.groq.com/docs/openai
    super(apiKey, "https://api.groq.com/openai/v1/");
  }
}

export const groqQuery = async (
  body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
) => {
  logger.debug("[groq] Req: %o", body);
  const groq = new GroqLLM(env.GROQ_API_KEY);
  const response = await groq.query(body);
  logger.debug("[groq] Res: %o", response);
  return response;
};
