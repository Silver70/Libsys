#!/usr/bin/env python3
"""
Modern SSL server for HSTS demonstration with Python 3.13 compatibility
"""
import os
import sys
import django
import ssl
import socket
from datetime import datetime, timezone, timedelta
from wsgiref.simple_server import make_server
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import ipaddress

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_self_signed_cert():
    """Create a self-signed certificate for demo purposes"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Demo"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Demo City"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Demo Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    return cert, private_key

def create_ssl_context():
    """Create SSL context with self-signed certificate"""
    # Create certificate and key
    cert, private_key = create_self_signed_cert()
    
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Convert certificate and key to PEM format
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Save certificate and key to temporary files
    import tempfile
    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    
    cert_file.write(cert_pem)
    key_file.write(key_pem)
    cert_file.close()
    key_file.close()
    
    # Load certificate and key into context
    context.load_cert_chain(cert_file.name, key_file.name)
    
    return context

def run_secure_server():
    """Run the secure server with HSTS headers and static file support"""
    from django.core.wsgi import get_wsgi_application
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    
    # Get the WSGI application
    application = get_wsgi_application()
    
    # Wrap with StaticFilesHandler for development
    application = StaticFilesHandler(application)
    
    # Create SSL context
    ssl_context = create_ssl_context()
    
    # Create server
    server = make_server('127.0.0.1', 8443, application)
    
    # Wrap socket with SSL
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    
    print("🔒 Starting Secure Development Server...")
    print("=" * 50)
    print("📍 Server URL: https://127.0.0.1:8443/")
    print("🔐 Protocol: HTTPS with HSTS")
    print("📁 Static files: Enabled")
    print("⚠️  Note: Browser will show security warning (self-signed certificate)")
    print("   Click 'Advanced' and 'Proceed to localhost (unsafe)' to continue")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        server.shutdown()

if __name__ == '__main__':
    run_secure_server() 