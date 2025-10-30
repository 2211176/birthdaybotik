from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CurrencyRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), unique=True, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

def get_rates_from_api():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        response.raise_for_status()
        return response.json()['rates']
    except Exception as e:
        raise Exception(f"Ошибка при подключении к API: {str(e)}")

@app.route('/update_rates')
def update_rates():
    try:
        rates = get_rates_from_api()
        for currency, rate in rates.items():
            existing = CurrencyRate.query.filter_by(currency=currency).first()
            if existing:
                existing.rate = rate
                existing.last_updated = datetime.utcnow()
            else:
                db.session.add(CurrencyRate(currency=currency, rate=rate))
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/last_update')
def last_update():
    last_record = CurrencyRate.query.order_by(CurrencyRate.last_updated.desc()).first()
    return jsonify({'last_update': last_record.last_updated.isoformat() if last_record else None})

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    from_curr = data['from'].upper()
    to_curr = data['to'].upper()
    amount = float(data['amount'])

    from_rate = CurrencyRate.query.filter_by(currency=from_curr).first()
    to_rate = CurrencyRate.query.filter_by(currency=to_curr).first()

    if not from_rate or not to_rate:
        return jsonify({'error': 'Неверные коды валют'}), 400

    result = (amount / from_rate.rate) * to_rate.rate
    return jsonify({'result': round(result, 2)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)