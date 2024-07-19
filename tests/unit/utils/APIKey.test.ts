import { env } from "../../../src/config";
import { verifyApiKey } from "../../../src/utils/apiKey";
import { chance } from "../../setup";

describe("Utility: API Key Tests", (): void => {
  const storedAPIKey: string = env.WEBHOOK_API_KEY;

  it("should return true for matching keys", (): void => {
    const providedApiKey: string = env.WEBHOOK_API_KEY;
    const result: boolean = verifyApiKey(providedApiKey, storedAPIKey);

    expect(result).toBe(true);
  });

  it("should return false for mismatched keys", (): void => {
    const invalidProvidedApiKey: string = chance.string({
      length: storedAPIKey.length,
    }); // Invalid provided API key in base64
    const result: boolean = verifyApiKey(invalidProvidedApiKey, storedAPIKey);

    expect(result).toBe(false);
  });
});
