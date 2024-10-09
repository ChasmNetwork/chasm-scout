import { groqQuery } from "../integration/groq";
import { ollamaQuery } from "../integration/ollama";
import { openAiQuery } from "../integration/openai";
import { openRouterQuery } from "../integration/openrouter";
import { vllmQuery } from "../integration/vllm";
import { logger } from "./logger";

export enum LLMProvider {
  GROQ = "groq",
  OPENAI = "openai",
  OPENROUTER = "openrouter",
  OLLAMA = "ollama",
  VLLM = "vllm",
}

export type QueryFunction =
  | typeof groqQuery
  | typeof openAiQuery
  | typeof openRouterQuery;

export const getLlmQuery = (provider: LLMProvider): QueryFunction => {
  const queryFunctions: Record<LLMProvider, QueryFunction> = {
    [LLMProvider.GROQ]: groqQuery,
    [LLMProvider.OPENAI]: openAiQuery,
    [LLMProvider.OPENROUTER]: openRouterQuery,
    [LLMProvider.OLLAMA]: ollamaQuery,
    [LLMProvider.VLLM]: vllmQuery,
  };

  return queryFunctions[provider];
};

export const getModelName = (provider: LLMProvider, model: string): string => {
  const modelMap: Record<string, Partial<Record<LLMProvider, string>>> = {
    "gemma2-9b-it": {
      [LLMProvider.GROQ]: "gemma2-9b-it",
      [LLMProvider.OPENROUTER]: "google/gemma-2-9b-it",
      [LLMProvider.OLLAMA]: "gemma2:9b",
      [LLMProvider.VLLM]: "google/gemma-2-9b-it",
    },
    "gemma-7b-it": {
      [LLMProvider.GROQ]: "gemma-7b-it",
      [LLMProvider.OPENROUTER]: "google/gemma-7b-it",
      [LLMProvider.OLLAMA]: "gemma:7b",
    },
    "gpt-3.5-turbo-0125": {
      [LLMProvider.OPENAI]: "gpt-3.5-turbo-0125",
    },
    "gpt-3.5-turbo": {
      [LLMProvider.OPENAI]: "gpt-3.5-turbo-0125",
    },
    "gpt-4-turbo": {
      [LLMProvider.OPENAI]: "gpt-4-turbo-2024-04-09",
    },
    "gpt-4-turbo-2024-04-09": {
      [LLMProvider.OPENAI]: "gpt-4-turbo-2024-04-09",
    },
    "gpt-4": {
      [LLMProvider.OPENAI]: "gpt-4-0613",
    },
    "gpt-4-0613": {
      [LLMProvider.OPENAI]: "gpt-4-0613",
    },
  };

  const modelForProvider = modelMap[model];
  if (!modelForProvider || !modelForProvider[provider]) {
    const errorMessage = `Model not found for provider ${provider} and model ${model}`;
    logger.error(errorMessage);
    throw new Error(errorMessage);
  }

  return modelForProvider[provider]!;
};
