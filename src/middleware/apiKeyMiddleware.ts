import { NextFunction, Request, Response } from "express";

import { env } from "../config";
import { verifyApiKey } from "../utils/apiKey";

export const apikeyAuthMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  const authorization = req.headers.authorization;
  const apiKey = authorization ? authorization.split(" ")[1] : null;

  if (!apiKey) {
    res.status(401).json({ message: "Unauthorized" });
    return;
  }

  try {
    const valid = verifyApiKey(apiKey, env.WEBHOOK_API_KEY);

    if (valid) {
      next();
    } else {
      res.status(401).json({ message: "Unauthorized" });
    }
  } catch (error: any) {
    res.status(400).json({ message: error.message });
  }
};
