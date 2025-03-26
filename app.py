import ipaddress
from flask import Flask, request, render_template

app = Flask(__name__)

# Replace this with your actual public IP or subnet (e.g., "145.654.435.1" or "145.654.0.0/16")
ALLOWED_ORG_IP = ipaddress.ip_network("103.177.0.0/16", strict=False)

def get_client_ip():
    """Retrieve real client public IP."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    client_ip = ip.split(",")[0].strip()  # First IP in case of multiple proxies
    return client_ip

def is_allowed(ip):
    """Check if an IP belongs to the organization's public network."""
    return ipaddress.ip_address(ip) in ALLOWED_ORG_IP

@app.route('/')
def home():
    client_ip = get_client_ip()
    if is_allowed(client_ip):
        message = f"✅ Yes, Allowed! Your Public IP: {client_ip}"
    else:
        message = f"❌ No, Not Allowed! Your Public IP: {client_ip}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
