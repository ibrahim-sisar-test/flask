from flask import Flask, request, jsonify
import math
import os

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    # تحويل الدرجات إلى راديان
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # حساب الفرق بين الإحداثيات
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # حساب المسافة باستخدام معادلة هافرسين
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # نصف قطر الأرض بالكيلومترات

    return distance

@app.route('/distance', methods=['GET'])
def get_distance():
    try:
        # استرجاع البيانات من الطلب
        lat1 = float(request.args.get('lat1'))
        lon1 = float(request.args.get('lon1'))
        lat2 = float(request.args.get('lat2'))
        lon2 = float(request.args.get('lon2'))

        # حساب المسافة
        distance = haversine(lat1, lon1, lat2, lon2)

        # إرجاع النتيجة
        return jsonify({'distance_km': round(distance, 2)})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway سيحدد البورت المناسب تلقائيًا
    app.run(host='0.0.0.0', port=port, debug=True)
