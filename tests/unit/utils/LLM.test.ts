import { groqQuery } from "../../../src/integration/groq";
import { ollamaQuery } from "../../../src/integration/ollama";
import { openAiQuery } from "../../../src/integration/openai";
import { openRouterQuery } from "../../../src/integration/openrouter";
import { getLlmQuery, getModelName, LLMProvider } from "../../../src/utils/llm";

describe("Utility: LLM Tests", (): void => {
  it("should throw error for unknown provider", (): void => {
    const unknownProvider: LLMProvider = "unknown_provider" as LLMProvider;

    expect(getLlmQuery(unknownProvider)).toBeUndefined();
  });

  it("should return correct query function for each provider", (): void => {
    expect(getLlmQuery(LLMProvider.GROQ)).toBe(groqQuery);
    expect(getLlmQuery(LLMProvider.OPENAI)).toBe(openAiQuery);
    expect(getLlmQuery(LLMProvider.OPENROUTER)).toBe(openRouterQuery);
    expect(getLlmQuery(LLMProvider.OLLAMA)).toBe(ollamaQuery);
  });

  it("should throw error for unknown provider", (): void => {
    const unknownProvider: LLMProvider = "unknown_provider" as LLMProvider;
    const knownModel: string = "gemma-7b-it";
    const expectedErrorMessage: string = `Model not found for provider ${unknownProvider} and model ${knownModel}`;

    expect(() => getModelName(unknownProvider, knownModel)).toThrow(
      expectedErrorMessage,
    );
  });

  it("should throw error for unknown model for a provider", (): void => {
    const knownProvider: LLMProvider.GROQ = LLMProvider.GROQ;
    const unknownModel: string = "unknown_model";
    const expectedErrorMessage: string = `Model not found for provider ${knownProvider} and model ${unknownModel}`;

    expect(() => getModelName(knownProvider, unknownModel)).toThrow(
      expectedErrorMessage,
    );
  });

  it("should return correct model name for known provider and model", (): void => {
    expect(getModelName(LLMProvider.GROQ, "gemma-7b-it")).toBe("gemma-7b-it");
    expect(getModelName(LLMProvider.OPENROUTER, "gemma-7b-it")).toBe(
      "google/gemma-7b-it",
    );
    expect(getModelName(LLMProvider.OLLAMA, "gemma-7b-it")).toBe("gemma:7b");
    expect(getModelName(LLMProvider.OPENAI, "gpt-3.5-turbo")).toBe(
      "gpt-3.5-turbo-0125",
    );
    expect(getModelName(LLMProvider.OPENAI, "gpt-4-turbo")).toBe(
      "gpt-4-turbo-2024-04-09",
    );
    expect(getModelName(LLMProvider.OPENAI, "gpt-4")).toBe("gpt-4-0613");
  });
});
