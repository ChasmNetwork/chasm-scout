import { Request, Response } from "express";
import OpenAI from "openai";
import { Stream } from "openai/streaming";

import { env } from "../config";
import { getLlmQuery, getModelName } from "../utils/llm";
import { logger } from "../utils/logger";

export const webhook =
  (openAiCompatible: boolean = false) =>
  async (req: Request, res: Response) => {
    const { body } = req.body;
    let requestBody;

    if (openAiCompatible) {
      requestBody = req.body;
    } else {
      requestBody = JSON.parse(body);
    }
    const model = requestBody.model;

    let result:
      | OpenAI.Chat.Completions.ChatCompletion
      | Stream<OpenAI.Chat.Completions.ChatCompletionChunk>
      | null = null;
    let usedProvider = "";
    let usedModel = "";

    try {
      for (let i = 0; i < env.PROVIDERS.length; i++) {
        const provider = env.PROVIDERS[i];

        try {
          const llmQuery = getLlmQuery(provider);
          const modelName = getModelName(provider, model);
          result = await llmQuery({
            ...requestBody,
            model: modelName,
          });
          usedProvider = provider;
          usedModel = modelName;
          if (result instanceof Stream) {
            res.setHeader("Content-Type", "text/event-stream");
            res.setHeader("Cache-Control", "no-cache");
            res.setHeader("Connection", "keep-alive");
            try {
              for await (const chunk of result) {
                const chunkData = JSON.stringify({
                  ...chunk,
                  scout: {
                    provider: usedProvider,
                    model: usedModel,
                  },
                });
                res.write(`data: ${chunkData}\n\n`);
              }
              res.write(`data: [DONE]\n\n`);
            } catch (streamErr) {
              logger.error("Error while streaming", streamErr);
            } finally {
              res.end(); // Ensure response is properly ended if an error occurs during streaming
            }
            return;
          }
          break;
        } catch (err) {
          logger.error("Provider failed", provider);
          logger.error(err);
        }
      }

      if (!result) {
        return res.status(500).send({ error: "All providers failed" });
      }

      return res.status(200).send({
        ...result,
        scout: {
          provider: usedProvider,
          model: usedModel,
        },
      });
    } catch (err) {
      logger.error(err);
      return res.status(500).send({ error: "Internal Server Error" });
    }
  };
