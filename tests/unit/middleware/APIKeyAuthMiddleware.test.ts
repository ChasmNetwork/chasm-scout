import { NextFunction, Request, Response } from "express";

import { env } from "../../../src/config";
import { apikeyAuthMiddleware } from "../../../src/middleware/apiKeyMiddleware";
import * as apiKey from "../../../src/utils/apiKey";

// Mock Express Request and Response objects
const mockRequest = {
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
} as Request;
const mockResponse = {
  status: jest.fn().mockReturnThis(),
  json: jest.fn(),
} as unknown as Response;
const mockNext = jest.fn() as NextFunction;

describe("API Key Auth Middleware Tests", (): void => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should return 401 Unauthorized if no API key is provided", async (): Promise<void> => {
    // Mock request headers
    mockRequest.headers = {};

    // Act
    await apikeyAuthMiddleware(mockRequest, mockResponse, mockNext);

    // Assert
    expect(mockResponse.status).toHaveBeenCalledWith(401);
    expect(mockResponse.json).toHaveBeenCalledWith({ message: "Unauthorized" });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it("should return 401 Unauthorized if API key is invalid", async (): Promise<void> => {
    // Arrange
    const invalidApiKey: string = "invalid-api-key";
    const middleware = apikeyAuthMiddleware;

    // Mock request headers
    mockRequest.headers = {
      authorization: `Bearer ${invalidApiKey}`,
    };

    // Act
    await middleware(mockRequest, mockResponse, mockNext);

    // Assert
    expect(mockResponse.status).toHaveBeenCalledWith(401);
    expect(mockResponse.json).toHaveBeenCalledWith({ message: "Unauthorized" });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it("should return 400 Bad Request if an error occurs during verification", async (): Promise<void> => {
    // Arrange
    const errorMessage: string = "Verification failed";

    // Mock request headers
    mockRequest.headers = {
      authorization: `Bearer invalid-api-key`,
    };

    // Override the actual verification to simulate hitting error
    jest.spyOn(apiKey, "verifyApiKey").mockImplementationOnce(() => {
      throw new Error(errorMessage);
    });

    // Act
    await apikeyAuthMiddleware(mockRequest, mockResponse, mockNext);

    // Assert
    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith({ message: errorMessage });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it("should call next() if API key is valid", async (): Promise<void> => {
    // Mock request headers
    mockRequest.headers = {
      authorization: `Bearer ${env.WEBHOOK_API_KEY}`,
    };

    // Act
    await apikeyAuthMiddleware(mockRequest, mockResponse, mockNext);

    // Assert
    expect(mockResponse.status).not.toHaveBeenCalled();
    expect(mockResponse.json).not.toHaveBeenCalled();
    expect(mockNext).toHaveBeenCalled();
  });
});
