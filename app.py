from flask import Flask, request, render_template
import ipaddress

app = Flask(__name__)

# Define the allowed subnet (change this to match your organization's network)
ORG_NETWORK = ipaddress.ip_network("192.168.137.1/24", strict=False)

def get_client_ip():
    """Retrieve the real client IP, considering proxies."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    client_ip = ip.split(",")[0].strip()  # Take the first IP (original client)
    return client_ip

def is_allowed(ip):
    """Check if an IP belongs to the organization's network."""
    return ipaddress.ip_address(ip) in ORG_NETWORK

@app.route('/')
def home():
    client_ip = get_client_ip()
    if is_allowed(client_ip):
        message = f"✅ Yes, Allowed! Your IP: {client_ip}"
    else:
        message = f"❌ No, Not Allowed! Your IP: {client_ip}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
