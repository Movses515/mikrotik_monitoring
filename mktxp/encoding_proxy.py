"""
Proxy that sits between mktxp and Prometheus.
Fetches metrics from mktxp, converts Windows-1251 garbled labels to UTF-8.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import re
import os

MKTXP_URL = os.environ.get("MKTXP_URL", "http://127.0.0.1:49091/metrics")
LISTEN_PORT = int(os.environ.get("PROXY_PORT", "49090"))


def fix_encoding(text):
    """
    mktxp reads RouterOS API strings as raw bytes and decodes them as UTF-8.
    When the router stores names in Windows-1251, the result is mojibake:
    each Win-1251 byte is interpreted as a Latin-1 char.
    Fix: encode back to Latin-1 (to recover original bytes), then decode as Windows-1251.
    """
    def convert_match(match):
        original = match.group(0)
        try:
            raw_bytes = original.encode('latin-1')
            return raw_bytes.decode('cp1251')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return original

    return re.sub(r'[\x80-\xff]+', convert_match, text)


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with urllib.request.urlopen(MKTXP_URL, timeout=30) as resp:
                raw = resp.read()
                text = raw.decode('utf-8', errors='replace')
                fixed = fix_encoding(text)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(fixed.encode('utf-8'))
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode('utf-8'))

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", LISTEN_PORT), ProxyHandler)
    print(f"Encoding proxy listening on :{LISTEN_PORT}, forwarding to {MKTXP_URL}")
    server.serve_forever()
