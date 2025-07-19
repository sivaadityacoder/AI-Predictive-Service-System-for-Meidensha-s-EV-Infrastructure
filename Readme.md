# Predictive AI Service System for Meidensha EV Infrastructure

### **Project Vision**
This project is a professional-grade prototype of a real-time, autonomous maintenance system for Meidensha's growing network of EV charging stations. It demonstrates a proactive, data-driven approach to field service, designed to enhance reliability, protect brand reputation, and reduce operational costs. Instead of reacting to failures, this system predicts them and initiates a service workflow automatically.

### **Core Workflow**
The system operates on a continuous, real-time loop:
1.  **Monitor:** Simulates a live stream of IoT sensor data from an EV charging station (`Voltage`, `Temperature`, `RPM`, etc.).
2.  **Predict:** A Machine Learning model (`IsolationForest`) trained on normal operational data analyzes the live stream to detect subtle anomalies that predict an impending component failure.
3.  **Diagnose & Dispatch (AI):** Upon detecting a predictive alert, the system sends the contextual data to Google's Gemini Pro AI. The AI, acting as a specialized service dispatcher named 'Meiden-AI', performs a root cause analysis and generates a structured, professional service ticket in JSON format.
4.  **Display:** The live status and the AI-generated service ticket are displayed on a real-time terminal dashboard.

### **Technology Stack**
* **Language:** Python
* **Machine Learning:** Scikit-learn (`IsolationForest`)
* **Generative AI:** Google Gemini Pro API (`google-generativeai`)
* **Data Handling:** Pandas
* **Database (Logging):** SQLite (Implicit, as a next step)
* **UI:** Colorama for a rich terminal interface

### **Live Demo**
*(Record a GIF of your terminal running the `main_ev.py` script and embed it here! Show the status changing from NORMAL to PREDICTIVE FAILURE ALERT and the AI ticket being generated.)*
![Demo GIF](your_demo_gif.gif)

### **How to Run**
1.  Clone the repository:
    ```bash
    git clone [https://github.com/YourUsername/meidensha-dx-project.git](https://github.com/YourUsername/meidensha-dx-project.git)
    cd meidensha-dx-project
    ```
2.  Set up the environment and install dependencies:
    ```bash
    python -m venv venv
    # Activate the environment
    pip install -r requirements.txt
    ```
3.  Set your Gemini API Key as an environment variable:
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
4.  Generate the training data and train the model:
    ```bash
    python create_ev_data.py
    python train_ev_model.py
    ```
5.  Run the main application:
    ```bash
    python main_ev.py
    ```
