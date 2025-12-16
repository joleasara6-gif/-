from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def is_valid_ip(ip):
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip):
        parts = ip.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            return True
    
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    if re.match(ipv6_pattern, ip):
        return True
    
    return False

@app.route('/xGeTinFo', methods=['GET'])
def get_ip_info():
    ip = request.args.get('ip')

    if not ip:
        ip = request.remote_addr
    

    if not is_valid_ip(ip):
        return jsonify({"error": "Invalid IP address"}), 400
    
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        

        if response.status_code != 200:
            return jsonify({"error": "Failed to get IP information"}), 400
        
        data = response.json()
        

        if data.get('error'):
            return jsonify({"error": "Invalid IP address or no information available"}), 400
        
        filtered_data = {
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country'),
            "loc": data.get('loc'),
            "org": data.get('org'),
            "timezone": data.get('timezone')
        }
        

        if all(value is None for value in filtered_data.values()):
            return jsonify({"error": "No information available for this IP"}), 400
        
        return jsonify(filtered_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Network error occurred"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

# إزالة app.run() للاستخدام على Vercel
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
