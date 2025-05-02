# Python Forced HHTP Codes - App

Tis application will return http error codes based on "mocked" JSON variables being sent - it's used to generate http error codes only.
  $~$ 
     

## Running with Podman
* podman build -t "APPNAME" .     
* podman run -p 5000:5000 "APPNAME"

## Running with Docker
* docker build -t "APPNAME" .
* docker run -p 5000:5000 "APPNAME"

## Running the application
* pip install -r requirements.txt
* flask run --host=0.0.0.0 --port=8080


## Testing

### 200 OK
curl -X POST http://your-server-address/api/check \
  -H "Content-Type: application/json" \
  -d '{"date": "04/10/2025", "vendor": "acme", "amt": 30000, "amount": 30000}'


### 500 Abort
curl -X POST http://your-server-address/api/check \
  -H "Content-Type: application/json" \
  -d '{"date": "04/10/2025", "vendor": "acme", "amt": 2000, "amount": 2000}'