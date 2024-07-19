import chalk from "chalk";
import WebSocket from "ws";

import { env } from "../config";
import { logger } from "../utils/logger";
import { getVersion } from "../utils/version";

const {
  IP,
  HANDSHAKE_PROTOCOL,
  ORCHESTRATOR_URL,
  SCOUT_NAME,
  SCOUT_UID,
  WEBHOOK_API_KEY,
  WEBHOOK_URL,
  PROVIDERS,
  MODEL,
} = env;

export async function handshake() {
  if (!ORCHESTRATOR_URL) {
    throw new Error("Please set the ORCHESTRATOR_URL environment variable");
  }

  logger.debug("Connecting to orchestrator at " + ORCHESTRATOR_URL);

  const ws = new WebSocket(
    `${HANDSHAKE_PROTOCOL}://${ORCHESTRATOR_URL.split("//")[1]}?uid=${SCOUT_UID}`,
    {
      headers: {
        Authorization: `Bearer ${WEBHOOK_API_KEY}`,
      },
    },
  );

  ws.on("open", function open() {
    logger.debug("Initiated WS handshake");

    logger.info(`Setting up webhook at: ${WEBHOOK_URL}`);
    ws.send(
      JSON.stringify({
        type: "webhook",
        webhookUrl: WEBHOOK_URL,
        ip: IP,
        version: getVersion(),
        name: SCOUT_NAME,
        providers: PROVIDERS,
        model: MODEL,
      }),
    );
  });

  ws.on("error", (error) => {
    throw new Error(
      `Handshake failed: ${error.message}\n${JSON.stringify(error, null, 2)}`,
    );
  });

  ws.on("close", (code, reason) => {
    if (code !== 1000) {
      throw new Error(
        `❌ Handshake with orchestrator at ${ORCHESTRATOR_URL} failed with error:\n${reason}`,
      );
    }
    logger.debug(`WS connection closed by the server with ${code}`);
  });

  ws.on("message", function incoming(data) {
    const { success } = JSON.parse(data.toString());
    if (success) {
      logger.info(
        chalk.green.bold(
          `✅ Handshake with orchestrator at ${ORCHESTRATOR_URL} complete`,
        ),
      );
      ws.close();
      return;
    } else {
      throw new Error(
        "❌ Handshake with orchestrator failed. No response from server.",
      );
    }
  });
}
