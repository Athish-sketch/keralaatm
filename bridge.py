from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import holidays

app = Flask(__name__)
CORS(app)

# Initialize Kerala State Holiday Matrix for regional regulatory compliance
kl_holidays = holidays.India(subdiv='KL')

@app.route('/predict_risk', methods=['POST'])
def predict_risk():
    data = request.json
    current_balance = float(data.get('current_balance', 0))
    proposed_deposit = float(data.get('proposed_deposit', 0))
    tier = data.get('tier', 'Rural')
    
    total_post_pool = current_balance + proposed_deposit
    remaining_cash = total_post_pool
    
    # Base daily historical drain configuration by tier
    tier_drain_map = {'Urban': 800000, 'Semi-Urban': 500000, 'Rural': 300000}
    base_drain = tier_drain_map.get(tier, 300000)
    
    today = datetime.now()
    days_lasted = 0.0
    holidays_encountered = []
    
    # Forward-Looking Sequential Calendar Simulation Loop (30-Day Window)
    for i in range(1, 31):
        future_date = today + timedelta(days=i)
        
        # Evaluate day structural constraints
        day_of_week = future_date.weekday()
        is_weekend = 1 if day_of_week in [5, 6] else 0
        is_payday = 1 if future_date.day >= 28 or future_date.day <= 5 else 0
        is_holiday = 1 if future_date in kl_holidays else 0
        
        # Calculate compounded velocity multiplier for this specific future date
        day_velocity = 1.0
        if is_weekend: day_velocity += 0.3
        if is_payday:  day_velocity += 0.5
        if is_holiday: 
            day_velocity += 0.7
            holidays_encountered.append(f"{future_date.strftime('%d-%b')}: {kl_holidays.get(future_date)}")
            
        daily_drain = base_drain * day_velocity
        
        if remaining_cash >= daily_drain:
            remaining_cash -= daily_drain
            days_lasted += 1.0
        else:
            # Calculate fractional day depletion value
            days_lasted += round(remaining_cash / daily_drain, 1)
            remaining_cash = 0
            break

    # Risk Flag Evaluation Engine based on calendar pressure vectors
    risk_status = "OPTIMAL SYSTEM LIQUIDITY"
    color_badge = "green"
    message = f"The injected capital structure is secure and estimated to sustain operations for {days_lasted} days."
    
    # CRITICAL TRIGGER: Cash runs out quickly AND upcoming regional holidays are detected
    if days_lasted < 3.0 and len(holidays_encountered) > 0:
        risk_status = "CRITICAL LIQUIDITY DEFICIT (HOLIDAY DRY RISK)"
        color_badge = "red"
        message = f"CRITICAL WARNING: Deposited capital will drain in {days_lasted} days, running dry BEFORE upcoming bank holiday blocks clear. Immediate armored dispatch required."
    elif days_lasted < 1.5:
        risk_status = "LIQUIDITY RUN-DRY ALERT"
        color_badge = "red"
        message = "Cash reserves will drop below baseline operational thresholds within 36 hours."
    elif days_lasted > 5.0:
        risk_status = "IDLE CAPITAL HOARD DETECTED"
        color_badge = "orange"
        message = "Excessive liquidity depth. Capital is locked up earning zero treasury yield interest."

    return jsonify({
        "total_post_pool": total_post_pool,
        "days_lasted": days_lasted,
        "upcoming_holidays_detected": list(set(holidays_encountered))[:3],
        "risk_status": risk_status,
        "color_badge": color_badge,
        "message": message
    })

if __name__ == '__main__':
    # Binds dynamically to the port provided by the cloud environment
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)