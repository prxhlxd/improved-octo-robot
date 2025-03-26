from flask import Flask, request, render_template
import ipaddress

app = Flask(__name__)

# Define the allowed subnet (change this to match your organization's network)
BITS_0 = ipaddress.ip_network("14.98.244.193", strict=False)
BITS_1 = ipaddress.ip_network("103.177.232.33", strict=False)
BITS_2 = ipaddress.ip_network("182.75.45.1", strict=False)
BITS_3 = ipaddress.ip_network("182.75.45.1", strict=False)

def get_client_ip():
    """Retrieve the real client IP, considering proxies."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    client_ip = ip.split(",")[0].strip()  # Take the first IP (original client)
    return client_ip

def is_allowed(ip):
    """Check if an IP belongs to the organization's network."""
    a = ipaddress.ip_address(ip)
    return ((a in BITS_0) or (a in BITS_1) or (a in BITS_2) or (a in BITS_3))

@app.route('/')
def home():
    client_ip = get_client_ip()
    if is_allowed(client_ip):
        message = f"✅ Yes, Allowed! Your IP: {client_ip}"
    else:
        message = f"❌ No, Not Allowed! Your IP: {client_ip}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

