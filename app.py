from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/xGeTinFo', methods=['GET'])
def get_ip_info():
    ip = request.args.get('ip')
   
    if not ip:
        ip = request.remote_addr
    
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data = response.json()
        
        filtered_data = {
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country'),
            "loc": data.get('loc'),
            "org": data.get('org'),
            "timezone": data.get('timezone')
        }
        
        return jsonify(filtered_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"Error =>": f"{str(e)}"}), 500
    except Exception as e:
        return jsonify({"Error =>": f"{str(e)}"}), 500

# إزالة app.run() للاستخدام على Vercel
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
