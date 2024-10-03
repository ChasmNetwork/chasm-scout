import OpenAI from "openai";

import { env } from "../config";
import { logger } from "../utils/logger";
import { OpenAIBase } from "./OpenAIBase";

class VLLM extends OpenAIBase {
  constructor() {
    super("vllm", `${env.VLLM_URL}/v1`, false);
  }
}

export const vllmQuery = async (
  body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
) => {
  logger.debug("[vllm] Req: %o", body);
  const vllm = new VLLM();
  const modifedBody: typeof body = {
    ...body,
    messages: [
      {
        role: "user",
        content: createPromptFromMessages(body.messages),
      },
    ],
    logprobs: true,
    top_logprobs: 5,
  };

  const response = await vllm.query(modifedBody);
  logger.debug("[vllm] Res: %o", response);
  return response;
};

export const createPromptFromMessages = (
  messages: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming["messages"],
) => {
  return messages
    .map(
      (message) =>
        `<start_of_turn>${message.role}\n${message.content}<end_of_turn>`,
    )
    .join("\n");
};
