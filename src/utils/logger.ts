import "dotenv/config";

import chalk from "chalk";
import { createLogger, format, transports } from "winston";

const { combine, timestamp, label, printf, simple, splat } = format;

const consoleFormat = printf(({ level, message, label, timestamp }) => {
  const levelUpper = level.toUpperCase();
  switch (levelUpper) {
    case "DEBUG":
      message = chalk.magenta(message);
      level = chalk.white.bgMagentaBright.bold(level);
      break;

    case "INFO":
      message = message;
      level = chalk.bgGreenBright.bold(level);
      break;

    case "WARN":
      message = chalk.yellow(message);
      level = chalk.black.bgYellowBright.bold(level);
      break;

    case "ERROR":
      message = chalk.red(message);
      level = chalk.black.bgRedBright.bold(level);
      break;

    default:
      break;
  }
  return `${level} ${message}`;
});

const LOGGER_LEVEL = process.env.LOGGER_LEVEL || "info";
export const logger = createLogger({
  level: LOGGER_LEVEL,
  format: combine(format.splat(), consoleFormat),
  transports: [
    new transports.Console(),
    new transports.File({ filename: "combined.log" }),
  ],
});

logger.info(`Logger level set to ${chalk.bold(LOGGER_LEVEL)}\n`);
