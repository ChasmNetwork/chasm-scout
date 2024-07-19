import { Request, Response } from "express";

import { env } from "../../../src/config";
import { webhook } from "../../../src/server/webhook";
import { logger } from "../../../src/utils/logger";

// Mock the logger
jest.mock("../../../src/utils/logger", () => ({
  logger: {
    error: jest.fn(),
  },
}));

describe("Webhook Tests", (): void => {
  let req: Partial<Request>;
  let res: Partial<Response>;

  const setupMockConfig = (overrides: Record<string, string>): void => {
    jest.mock("../../../src/config", () => {
      const originalModule = jest.requireActual("../../../src/config");
      return {
        ...originalModule,
        env: {
          ...originalModule.env,
          ...overrides,
        },
      };
    });
  };

  const executeWebhook = async (
    req: Partial<Request>,
    res: Partial<Response>,
    openAiCompatible: boolean = true,
  ) => {
    const controller = webhook(openAiCompatible);
    await controller(req as Request, res as Response);
  };

  beforeEach((): void => {
    req = {
      body: {
        model: "gemma-7b-it",
        temperature: 0.7,
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
      },
    };

    res = {
      status: jest.fn().mockReturnThis(),
      send: jest.fn(),
      setHeader: jest.fn(),
      write: jest.fn(),
      end: jest.fn(),
    } as Partial<Response>;
  });

  afterEach((): void => {
    jest.clearAllMocks();
  });

  it("should handle error when getModelName encounters invalid model", async (): Promise<void> => {
    setupMockConfig({ MODEL: "mocked-model" });

    await executeWebhook(req, res);

    // Assert logging of "Provider failed" and the error message
    expect(logger.error).toHaveBeenCalledWith(
      "Provider failed",
      env.PROVIDERS[0],
    );

    // Assert response status and message
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.send).toHaveBeenCalledWith({ error: "All providers failed" });
  });

  it("should handle error when getModelName encounters invalid provider", async (): Promise<void> => {
    setupMockConfig({ PROVIDERS: "mocked-provider" });

    await executeWebhook(req, res);

    // Assert logging of "Provider failed" and the error message
    expect(logger.error).toHaveBeenCalledWith(
      "Provider failed",
      env.PROVIDERS[0],
    );

    // Assert response status and message
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.send).toHaveBeenCalledWith({ error: "All providers failed" });
  });
});
