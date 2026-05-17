# Locally Hosting [LOCAL TUNNEL]
- PASS WARNING BYPASS HEADER INTO THE API KEY CUSTOM HEADER OPTION IN `AUTHENTICATION` WITHIN CHATGPT ACTION SETTINGS GUI
- `npm install -g localtunnel`
- CLI
  - `lt --port 8000 --subdomain your-custom-subdomain`
- ``` yaml
  // * GPT SCHEMA *
  servers:
      - url: https://your-custom-subdomain.loca.lt
    ```

- ``` python
  # * DJANGO SETTINGS.PY *
  ALLOWED_HOSTS = ['your-custom-subdomain.loca.lt', 'localhost', '127.0.0.1']
  ```


# Locally Hosting [ NGROK ]
- PASS WARNING BYPASS HEADER INTO THE API KEY CUSTOM HEADER OPTION IN `AUTHENTICATION` WITHIN CHATGPT ACTION SETTINGS GUI
- go to ngrok website and install ngrok
- add auth token to ngrok cli 
- CLI
  - `ngrok http --domain=reasonably-fit-impala.ngrok-free.app 8000`
- ``` yaml
  // * GPT SCHEMA *
  servers:
      - url: https://reasonably-fit-impala.ngrok-free.app
    ```

- ``` python
  # * DJANGO SETTINGS.PY *
  ALLOWED_HOSTS = ['reasonably-fit-impala.ngrok-free.app', 'localhost', '127.0.0.1']
```