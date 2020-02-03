 def get_bundle(self, application_id):
        token = {
            "name": "webhook-name",
            "secret": "webhook-secret",
            "identifier": "webhook-identifier"
        }
 
        method      = 'GET'
        body        = ''
        root_url    = 'https://credfin.io'
        path        = '/api/applications/{}/bundle'.format(application_id)
        timestamp   = datetime.datetime.utcnow().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        contentType = 'application/json'
 
        hash = hashlib.md5(body.encode())
        contentMD5 = b64encode(hash.digest()).decode('utf-8')
        message_parts = [method, contentMD5, contentType, timestamp, path]
        message = '\n'.join(message_parts)
 
        signature = hmac.new(bytes(token['secret'], 'latin-1'), 
                    bytes(message, 'latin-1'), digestmod=hashlib.sha256)
        hmac_base64 = b64encode(signature.digest()).decode('utf-8')
 
        headers = {
            'Date': timestamp,
            'Content-MD5': contentMD5,
            'Content-Type': contentType,
            'Authorization': 'HMAC {}:{}'.format(token['identifier'], hmac_base64)
        }
 
        request = requests.Request(
            'GET', '{}{}'.format(root_url, path),
            data=body, headers=headers)
        prepped = request.prepare()
        prepped.headers = headers
 
        with requests.Session() as session:
            response = session.send(prepped)
 
        if response.status_code != 200:
            print("Bad status code: {}".format(response.status_code))
            print("Bad status: {}".format(response.text))
            print(root_url, path)
            raise()
 
        print('Retrieved bundle')
        bundle = response.json()
        return bundle