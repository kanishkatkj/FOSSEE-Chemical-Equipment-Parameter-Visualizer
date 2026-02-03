# Chemical Equipment Parameter Visualizer

A professional hybrid Web and Desktop application for visualizing and analyzing chemical equipment data.

## Features
- **Data Ingestion**: Robust CSV parsing for equipment data (Name, Type, Flowrate, Pressure, Temperature).
- **Statistical Analysis**: Instant calculation of counts, averages, and distributions.
- **Interactive Visualization**: 
  - **Web**: Responsive Chart.js visualizations (Donut & Bar charts).
  - **Desktop**: Native Matplotlib integrations.
- **History Management**: Tracks the last 5 uploaded datasets for quick access.
- **Reporting**: Automated PDF report generation with data summaries.
- **Cross-Platform Access**: Seamless experience across React Web App and PyQt5 Desktop Client, powered by a unified Django REST API.

---

## Tech Stack
- **Backend API**: Python, Django 5+, Django REST Framework, Pandas, SQLite.
- **Frontend Web**: React 19, Vite, Chart.js, Vanilla CSS (Modern Slate/Zinc Theme).
- **Frontend Desktop**: Python, PyQt5, Matplotlib, Requests.

---

## Setup Instructions

### Prerequisites
1. **Python**: Installed and added to PATH.
2. **Node.js**: Installed (for the web frontend).

### 1. Backend Setup (Django)
*The backend must be running for both apps to work.*

1. Open a **Terminal** (PowerShell) and navigate to the backend folder:
   ```powershell
   cd backend
   ```

2. **Establish Security Permissions** (If you see "scripts disabled" errors):
   Run this command one time to allow script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```
   *(Type 'A' and Enter if prompted)*

3. Create and Activate Virtual Environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   *(You should see `(venv)` at the start of the line)*

4. Install Dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Start the Server:
   ```powershell
   python manage.py runserver
   ```
   **Keep this terminal open!** The server is running at `http://127.0.0.1:8000/`.

### 2. Frontend Web Setup (React)
1. Open a **New Terminal**.

2. Navigate to the web folder:
   ```powershell
   cd frontend-web
   ```

3. Install Dependencies (First time only):
   ```powershell
   npm install
   ```

4. Start the Application:
   ```powershell
   npm run dev
   ```

5. Open the Link:
   - Hold `Ctrl` and click the link shown (e.g., `http://localhost:5173/`).

### 3. Frontend Desktop Setup (PyQt5)
1. Open a **New Terminal**.

2. Navigate to the desktop folder:
   ```powershell
   cd frontend-desktop
   ```

3. Install Dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Run the App:
   ```powershell
   python main.py
   ```

---

## Login Credentials
**Required Credentials (Case Sensitive):**
- **Username:** `Admin`
- **Password:** `Admin`

---

## Sample Data
Use the provided `sample_equipment_data.csv` in the root directory to test the file upload feature.
