import OpenAI from "openai";

import { env } from "../config";
import { logger } from "../utils/logger";

class OpenAILLM extends OpenAI {
  constructor(apiKey: string) {
    super({ apiKey });
  }
}

export const openAiQuery = async (
  body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
) => {
  logger.debug("[openai] Req: %o", body);
  const openai = new OpenAILLM(env.OPENAI_API_KEY);
  const response = await openai.chat.completions.create(body);
  logger.debug("[openai] Res: %o", response);
  return response;
};
