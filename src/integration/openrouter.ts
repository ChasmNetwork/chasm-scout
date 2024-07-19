import OpenAI from "openai";

import { env } from "../config";
import { logger } from "../utils/logger";
import { OpenAIBase } from "./OpenAIBase";

class OpenRouterLLM extends OpenAIBase {
  constructor(apiKey: string) {
    super(apiKey, "https://openrouter.ai/api/v1");
  }
}

export const openRouterQuery = async (
  body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
) => {
  const newBody = {
    ...body,
    ...env.OPENROUTER_CUSTOM_CONFIG,
  };
  logger.debug("[openrouter] Req: %o", newBody);
  const or = new OpenRouterLLM(env.OPENROUTER_API_KEY);
  const response = await or.query(newBody);
  logger.debug("[openrouter] Res: %o", response);
  return response;
};
