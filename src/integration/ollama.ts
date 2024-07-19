import OpenAI from "openai";

import { logger } from "../utils/logger";
import { OpenAIBase } from "./OpenAIBase";

class OllamaLLM extends OpenAIBase {
  constructor() {
    super("ollama", "http://localhost:11434/v1");
  }
}

export const ollamaQuery = async (
  body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
) => {
  logger.debug("[ollama] Req: %o", body);
  const ollama = new OllamaLLM();
  const response = await ollama.query(body);
  logger.debug("[ollama] Res: %o", response);
  return response;
};
