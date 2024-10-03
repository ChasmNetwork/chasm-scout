import OpenAI from "openai";
import { Stream } from "openai/streaming";

import { logger } from "../utils/logger";

export abstract class OpenAIBase {
  protected openai: OpenAI;

  constructor(
    apiKey: string,
    baseURL?: string,
    protected logProbs = false,
  ) {
    this.openai = new OpenAI({
      apiKey: apiKey,
      baseURL: baseURL,
    });
  }

  async query(
    body: OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming,
  ): Promise<
    | OpenAI.Chat.Completions.ChatCompletion
    | Stream<OpenAI.Chat.Completions.ChatCompletionChunk>
  > {
    const isStreaming = body.stream ?? false;
    try {
      const stream = await this.openai.chat.completions.create({
        ...body,
        stream: true,
      });
      if (isStreaming) {
        return stream;
      } else {
        let accumulatedData = "";
        let accumulatedLogProbs: any[] = [];
        let completion: OpenAI.Chat.Completions.ChatCompletion | null = null;
        const usage = {
          prompt_tokens: 0,
          completion_tokens: 0,
          total_tokens: 0,
        };

        for await (const chunk of stream) {
          accumulatedData += chunk.choices[0].delta.content || "";
          if (this.logProbs)
            accumulatedLogProbs.push(chunk.choices[0].logprobs);
          completion = chunk as any;
          usage.completion_tokens += 1;
        }
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens;

        return {
          ...completion!,
          usage,
          choices: [
            {
              index: 0,
              message: {
                role: "assistant",
                content: accumulatedData,
              },
              finish_reason: "stop",
              logprobs: this.logProbs
                ? {
                    content: accumulatedLogProbs,
                  }
                : null,
            },
          ],
        };
      }
    } catch (error) {
      logger.debug("[base] Error: %o", error);
      throw error;
    }
  }
}
