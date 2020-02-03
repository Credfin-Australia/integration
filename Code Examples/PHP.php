public function rawApiCall($identifier, $secret, $method, $path, $body = '')
{
    $now = now();
    $token = [
        'secret' => $secret,
        'identifier' => $identifier,
    ];
    $root = 'https://credfin.io';

    $timestamp = $now->format('D, d M Y H:i:s')
    $contentType = 'application/json';
    $hash = md5($body, true);
    $contentMD5 = base64_encode($hash);
    $messageParts = [
        $method,
        $contentMD5,
        $contentType,
        $timestamp,
        $path,
    ];
    $message = implode("\n", $messageParts);
    $hash = hash_hmac('sha256', $message, $token['secret'], true);
    $hmacBase64 = base64_encode($hash);
    $headers = [
        'Date' => $timestamp,
        'Content-MD5' => $contentMD5,
        'Content-Type' => $contentType,
        'Authorization' => 'HMAC '.$token['identifier'].':'.$hmacBase64,
    ];
    $response = $this->client->request($method, $root.$path, [
        'verify' => false,
        'body' => $body ? $body : null,
        'headers' => $headers,
        'timeout' => 15
    ])->getBody()->getContents();
    $bytes = strlen($body);
    $secondsToRun = $now->diffInSeconds(now());
    return $response;
}