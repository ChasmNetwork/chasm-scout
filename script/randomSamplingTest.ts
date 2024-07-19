import { groqQuery } from "../src/integration/groq";
import { ollamaQuery } from "../src/integration/ollama";
import { openRouterQuery } from "../src/integration/openrouter";
import { getModelName, LLMProvider } from "../src/utils/llm";

const model = "gemma-7b-it";
const query: any = {
  messages: [
    {
      role: "system",
      content:
        "You are a helpful assistant. You are given a question and answer choices, please only pick one of the answer choice without explanation.",
    },
    {
      role: "user",
      content: `Question: Find the characteristic of the ring Z x Z.	
Answer Choices: [ "0", "3", "12", "30" ]	      
`,
    },
  ],
  seed: Math.floor(Math.random() * 10000),
  temperature: 0.1,
  model,
};

async function main() {
  const res = await Promise.all([
    ollamaQuery({
      ...query,
      model: getModelName(LLMProvider.OLLAMA, model),
    }),
    openRouterQuery({
      ...query,
      model: getModelName(LLMProvider.OPENROUTER, model),
    }),
    groqQuery({
      ...query,
      model: getModelName(LLMProvider.GROQ, model),
    }),
  ]);

  console.log(res);
}

main();
