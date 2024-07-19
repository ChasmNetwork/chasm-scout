export function verifyApiKey(
  providedApiKey: string,
  storedApiKey: string,
): boolean {
  const decodedProvidedApiKey = Buffer.from(providedApiKey, "base64").toString(
    "utf8",
  );
  const decodedStoredApiKey = Buffer.from(storedApiKey, "base64").toString(
    "utf8",
  );

  return decodedProvidedApiKey === decodedStoredApiKey;
}
