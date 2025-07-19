import os
import time
import random
import datetime
import json
import joblib
import pandas as pd
import google.generativeai as genai
from colorama import Fore, Style, init

# --- SETUP ---
init(autoreset=True)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found!")
genai.configure(api_key=API_KEY)
MODEL = joblib.load('ev_model.pkl')
FEATURES = ['voltage_output', 'current_draw', 'internal_coolant_temp', 'coolant_pump_rpm']

# --- GEMINI PROMPT FUNCTION ---
def create_ev_service_ticket_prompt(data):
    # Paste the full prompt function from our previous conversation here
    # It starts with: prompt = f""" You are 'Meiden-AI'... """
    # and ends with: return prompt
    prompt = f"""
    You are 'Meiden-AI', a specialized AI Service Dispatcher for Meidensha's advanced EV Charging Infrastructure.
    A predictive failure alert has been triggered for Charging Station #MDS-EV-1138 in Shizuoka. The system predicts a critical failure is likely within the next 72 hours.

    LIVE DATA LEADING TO THE ALERT:
    - Timestamp: {data['timestamp']}
    - Voltage Output: {data['voltage']}V (Stable)
    - Internal Coolant Temp: {data['temp']}°C (Trending upwards)
    - Coolant Pump RPM: {data['rpm']} RPM (Trending upwards, indicating strain)

    YOUR TASK:
    Generate a complete, structured service ticket for a field technician to proactively prevent a public failure. Format your response as a single, valid JSON object.
    The JSON must contain these exact keys: "ticket_id", "station_id", "urgency_level", "predicted_failure_mode", "required_parts" (an array of objects), "service_instructions" (an array of strings), "technician_notes".
    """
    return prompt

# --- GEMINI API CALL FUNCTION ---
def get_ai_service_ticket(data):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = create_ev_service_ticket_prompt(data)
        # Add generation_config to ask for JSON output
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Gemini API Error: {e}"}

# --- SIMULATION & DISPLAY FUNCTIONS ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def simulate_live_data(is_anomaly=False):
    if not is_anomaly:
        return {'voltage_output': random.uniform(478, 482), 'current_draw': random.uniform(28, 32), 'internal_coolant_temp': random.uniform(68, 75), 'coolant_pump_rpm': random.uniform(1450, 1550)}
    else:
        return {'voltage_output': random.uniform(478, 482), 'current_draw': random.uniform(28, 32), 'internal_coolant_temp': random.uniform(88, 95), 'coolant_pump_rpm': random.uniform(1800, 2000)}

def display_dashboard(status, data, analysis_ticket):
    clear_screen()
    status_color = Fore.GREEN if status == "NORMAL" else Fore.RED
    print(Fore.CYAN + Style.BRIGHT + "="*80)
    print("      MEIDENSHA EV CHARGING STATION - AUTONOMOUS PREDICTIVE MAINTENANCE SYSTEM")
    print(Fore.CYAN + Style.BRIGHT + "="*80)
    print(f"STATION ID: MDS-EV-1138 (Shizuoka)   |   SYSTEM STATUS: {status_color}{status}{Style.RESET_ALL}")
    print("-"*80)
    print(Fore.YELLOW + "--- LIVE SENSOR DATA ---")
    for key, value in data.items():
        print(f"{key.replace('_', ' ').title():<25}: {value:.2f}")
    print("\n" + Fore.YELLOW + "--- MEIDEN-AI SERVICE TICKET ---")
    if isinstance(analysis_ticket, dict) and "error" not in analysis_ticket:
        print(f"{Fore.CYAN}Ticket ID: {analysis_ticket.get('ticket_id', 'N/A')}")
        print(f"{Fore.RED}Urgency: {analysis_ticket.get('urgency_level', 'N/A')}")
        print(f"{Style.RESET_ALL}Predicted Failure: {analysis_ticket.get('predicted_failure_mode', 'N/A')}")
        print(f"{Style.RESET_ALL}Technician Notes: {analysis_ticket.get('technician_notes', 'N/A')}")
    else:
        print(analysis_ticket)
    print("\n" + Fore.CYAN + "="*80)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    counter = 0
    last_ticket = "System is initializing..."
    while True:
        is_anomaly = (counter > 5 and counter % 10 == 0)
        live_data = simulate_live_data(is_anomaly)
        df_live = pd.DataFrame([live_data])[FEATURES]
        prediction = MODEL.predict(df_live)

        if prediction[0] == -1:
            status = "PREDICTIVE FAILURE ALERT"
            prompt_data = {'timestamp': datetime.datetime.now().isoformat(), 'voltage': live_data['voltage_output'], 'temp': live_data['internal_coolant_temp'], 'rpm': live_data['coolant_pump_rpm']}
            ticket = get_ai_service_ticket(prompt_data)
            last_ticket = ticket
        else:
            status = "NORMAL"

        display_dashboard(status, live_data, last_ticket)
        counter += 1
        time.sleep(2)
