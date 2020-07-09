async function getFromAPI(path) {
  const token = {
    name: "xxxx",
    secret: "xxxx",
    identifier: "xxxx"
  };

  const method = "GET";
  const body = "";

  const root = "https://credfin.io";
  const timestamp = new Date().toUTCString();
  const contentType = "application/json";

  const hash = crypto.createHash("md5");
  hash.update(body);
  const contentMD5 = hash.digest("base64");

  const messageParts = [method, contentMD5, contentType, timestamp, path];
  const message = messageParts.join("\n");

  const hmac = crypto.createHmac("sha256", token.secret);
  hmac.update(message);
  const hmacBase64 = hmac.digest("base64");

  const headers = {
    DatetimeUtc: timestamp,
    "Content-MD5": contentMD5,
    "Content-Type": contentType,
    Authorization: `HMAC ${token.identifier}:${hmacBase64}`
  };

  const response = await fetch(root + path, {
    method,
    headers,
    body: body == "" ? null : body
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response;
}
