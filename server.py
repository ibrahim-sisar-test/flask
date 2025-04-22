import requests
from flask import Flask, request

app = Flask(__name__)

def get_location(ip):
    # استخدم API للحصول على الموقع الجغرافي
    api_key = '373de7d750b4df1ac901c8aa1520ea77'  # استبدل بمفتاح API الخاص بك
    url = f'http://api.ipstack.com/{ip}?access_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch location data"}

@app.route('/')
def gather_info():
    # الحصول على عنوان IP الخاص بالمستخدم
    user_ip = request.remote_addr

    # الحصول على HTTP Headers
    headers = request.headers

    # الحصول على نوع المتصفح (User-Agent)
    user_agent = headers.get('User-Agent', 'Unknown')

    # صفحة الإحالة (إذا كانت متوفرة)
    referrer = headers.get('Referer', 'No referrer available')

    # الحصول على الموقع التقريبي بناءً على عنوان IP
    location_data = get_location(user_ip)
    if "error" in location_data:
        location_info = "<p><strong>Location:</strong> Unable to fetch location data</p>"
    else:
        location_info = f"""
        <p><strong>Location Details:</strong></p>
        <ul>
            <li><strong>Country:</strong> {location_data.get('country_name', 'Unknown')}</li>
            <li><strong>City:</strong> {location_data.get('city', 'Unknown')}</li>
            <li><strong>Region:</strong> {location_data.get('region_name', 'Unknown')}</li>
            <li><strong>Latitude:</strong> {location_data.get('latitude', 'Unknown')}</li>
            <li><strong>Longitude:</strong> {location_data.get('longitude', 'Unknown')}</li>
        </ul>
        """

    # صياغة كافة المعلومات لعرضها
    info = f"""
    <h1>Collected Information</h1>
    <p><strong>Your IP Address:</strong> {user_ip}</p>
    <p><strong>Your Browser:</strong> {user_agent}</p>
    <p><strong>Referrer Page:</strong> {referrer}</p>
    {location_info}
    <p><strong>All Headers:</strong></p>
    <ul>
    """
    for header, value in headers.items():
        info += f"<li><strong>{header}:</strong> {value}</li>"
    info += "</ul>"

    return info

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))  # Railway سيحدد البورت المناسب تلقائيًا
     app.run(host='0.0.0.0', port=port, debug=True)
