from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json

# mohammad: this file runs the server and gets live rates from the internet
# mohammad: i watched like 3 videos to figure this out

# mohammad: these are backup rates just in case the internet doesnt work
# zack: good idea having a backup
backup_rates = {
    "USD": 1,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.5,
    "CAD": 1.36,
    "AUD": 1.53,
    "INR": 83.1,
    "SAR": 3.75,
    "AED": 3.67
}

# mohammad: this function goes online and gets the real rates
def get_live_rates():
    try:
        # mohammad: this website gives free rates no api key 
        url = "https://open.er-api.com/v6/latest/USD"
        response = urllib.request.urlopen(url, timeout=5)
        data = json.loads(response.read())

        if data["result"] == "success":
            print("mohammad: got live rates !!")
            return data["rates"]
        else:
            print("something went wrong, using backup rates")
            return backup_rates

    except Exception as e:
        # mohammad: if anything goes wrong just use the backup
        print("error getting rates:", e)
        print("using backup rates instead")
        return backup_rates

# mohammad: get the rates when the server starts
# suhail: i moved this line up here so it loads once at the start
current_rates = get_live_rates()

# mohammad: this handles all the requests from the browser
class MyHandler(BaseHTTPRequestHandler):

    # mohammad: this runs every time the browser asks for something
    def do_GET(self):

        # mohammad: serve the html file
        if self.path == "/" or self.path == "/index.html":
            try:
                # iad: i helped with opening the file correctly
                with open("currency_converter_simple.html", "rb") as f:
                    html = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html)

            except:
                # mohammad: if html file not found show error
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"html file not found, make sure currency_converter_simple.html is in the same folder")

        # mohammad: this sends the rates to the html page as json
        # zack: the html will call this to get live rates
        elif self.path == "/rates":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            # mohammad: this line allows the html to talk to python (i had an error without it lol)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = json.dumps(current_rates).encode()
            self.wfile.write(response)

              # mohammad: this part lets the server send images and other files to the browser
              # mohammad: without this image wouldn't show
        elif self.path.endswith(".webp"):
            try:
                with open(self.path[1:], "rb") as f:
                    image = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "image/webp")
                self.end_headers()
                self.wfile.write(image)

            except:
                self.send_response(404)
                self.end_headers()


        else:
            self.send_response(404)
            self.end_headers()

    # mohammad: this removes the annoying log messages in the terminal
    # suhail: actually keep them, its useful to see whats happening
    # mohammad: ok fine i commented it out
    # def log_message(self, format, *args):
    #     pass

# mohammad: start the server on port 8000
# zack: make sure nothing else is running on port 8000
server = HTTPServer(("", 8000), MyHandler)
print("server is running at http://localhost:8000")
print("press ctrl+c to stop")


server.serve_forever()
