import OpenAI from "openai";

import { env } from "../../src/config";
import { groqQuery } from "../../src/integration/groq";
import { getModelName, LLMProvider } from "../../src/utils/llm";

// Adding this cause sometimes the LLM takes time and the test will fail CI
// Default jest timeout is 5000 ms for a test
jest.setTimeout(60000);

describe("Groq Tests", (): void => {
  const provider: LLMProvider = env.PROVIDERS.filter(
    (provider: LLMProvider): boolean => provider === LLMProvider.GROQ,
  )[0];

  const model: string = getModelName(provider, env.MODEL);

  const payload = {
    temperature: 0.7,
    messages: [
      {
        role: "system",
        content: "You are a helpful assistant.",
      },
      {
        role: "user",
        content: "What is the sum of 1 and 2?",
      },
    ],
  } as unknown as Request;

  it("should return an answer that matches the query", async (): Promise<void> => {
    const response = await groqQuery({
      ...payload,
      model,
      stream: false,
    } as unknown as OpenAI.Chat.Completions.ChatCompletionCreateParamsNonStreaming);

    const content = (response as OpenAI.Chat.Completions.ChatCompletion)
      .choices[0].message.content as string;

    await expect(content).toSatisfyStatement(
      "It contains an answer to the sum of 1 and 2.",
    );
  });
});
