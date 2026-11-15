import time, random, json, os, threading
from flask import Flask, request, jsonify
app = Flask(__name__)
customers={}; otps={}; balances={"OUT-9302":{"spot":5000.0,"fut":5000.0}}
@app.route('/')
def home(): return jsonify({"app":"OUTWARD","status":"RUNNING","balance":balances["OUT-9302"]})
@app.route('/login', methods=['POST'])
def login():
    d=request.json; cid=d.get('customer_id'); customers[cid]=d
    return jsonify({"status":"OK","customer_id":cid,"balance":balances.get(cid)})
@app.route('/send_email_otp', methods=['POST'])
def se():
    d=request.json; e=d.get('email'); o=str(random.randint(100000,999999)); otps[f"e_{e}"]=o
    print(f"EMAIL OTP: {e} -> {o}"); return jsonify({"status":"SENT","demo_otp":o})
@app.route('/verify_email_otp', methods=['POST'])
def ve():
    d=request.json
    return jsonify({"status":"VERIFIED" if otps.get(f"e_{d.get('email')}")==d.get('otp') else "WRONG"})
@app.route('/send_mobile_otp', methods=['POST'])
def sm():
    d=request.json; m=d.get('mobile'); o=str(random.randint(100000,999999)); otps[f"m_{m}"]=o
    print(f"MOBILE OTP: {m} -> {o}"); return jsonify({"status":"SENT","demo_otp":o})
@app.route('/verify_mobile_otp', methods=['POST'])
def vm():
    d=request.json
    return jsonify({"status":"VERIFIED" if otps.get(f"m_{d.get('mobile')}")==d.get('otp') else "WRONG"})
@app.route('/subscribe', methods=['POST'])
def sub():
    d=request.json; return jsonify({"status":"SUBSCRIBED","plan":d.get('plan'),"live":True})
@app.route('/connect_broker', methods=['POST'])
def br():
    d=request.json; return jsonify({"status":"CONNECTED","broker":d.get('broker')})
@app.route('/save_token', methods=['POST'])
def tok():
    d=request.json; customers[d.get('customer_id')]=d
    return jsonify({"status":"SYNCED","bot":"RUNNING"})
@app.route('/balance/<cid>', methods=['GET'])
def bal(cid):
    b=balances.get(cid,{"spot":5000,"fut":5000}); return jsonify({"spot":b["spot"],"futures":b["fut"],"total":b["spot"]+b["fut"]})
@app.route('/market', methods=['GET'])
def mkt():
    return jsonify([{"name":"BTC","price":65462},{"name":"ETH","price":3420},{"name":"SOL","price":180},{"name":"DOGE","price":0.16},{"name":"XRP","price":0.52},{"name":"BNB","price":590},{"name":"EURUSD","price":1.08},{"name":"GBPUSD","price":1.27},{"name":"USDJPY","price":149.5},{"name":"XAUUSD","price":2030},{"name":"USOIL","price":78.5},{"name":"UKOIL","price":82.3}])
@app.route('/tables', methods=['GET'])
def tbl():
    return jsonify({"live_price":"RUNNING","profit_loss":"RUNNING","top_traders":"RUNNING","market_speed":"FAST+SLOW"})
def bot_runner():
    markets=["BTC","ETH","SOL","DOGE","XRP","BNB","EURUSD","GBPUSD","USDJPY","XAUUSD","USOIL","UKOIL"]
    futs=["BTCUSDT-PERP","ETHUSDT-PERP","SOLUSDT-PERP","DOGEUSDT-PERP","XRPUSDT-PERP","BNBUSDT-PERP"]
    c=0
    while True:
        c+=1; b=balances["OUT-9302"]
        if c%2==1:
            m=random.choice(markets); w=random.random()<0.75
            b["spot"]+=0.03 if w else -0.06
        else:
            m=random.choice(futs); w=random.random()<0.75
            b["fut"]+=0.30 if w else -0.60
        time.sleep(3)
threading.Thread(target=bot_runner, daemon=True).start()
if __name__=='__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
