import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const baseURL = new URL(process.env.WEBHOOK_URL!).toString() + "v1";
console.log(baseURL);

const openai = new OpenAI({
  baseURL,
  apiKey: process.env.WEBHOOK_API_KEY,
});

(async () => {
  console.log("Calling Stream\n");
  const result1 = await openai.chat.completions.create({
    stream: true,
    model: "gemma-7b-it",
    messages: [
      {
        role: "system",
        content: "You are a helpful assistant.",
      },
      {
        role: "user",
        content: "What is the meaning of life?",
      },
    ],
  });
  for await (const chunk of result1) {
    process.stdout.write(chunk.choices[0].delta.content || "");
  }
  console.log("\n---------------");
  console.log("\n\nCalling Non-Stream");
  const result2 = await openai.chat.completions.create({
    stream: false,
    model: "gemma2-9b-it",
    messages: [
      {
        role: "system",
        content: "You are a helpful assistant.",
      },
      {
        role: "user",
        content: "What is the meaning of life?",
      },
    ],
  });
  console.log(result2.choices[0].message.content);
  console.log("\n---------------");
  console.log((result2 as any).scout);
})();
