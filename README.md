# NurseGuard — Intelligent Nurse Fatigue Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Algorithm](https://img.shields.io/badge/Algorithm-NSGA--II-purple)
![ML](https://img.shields.io/badge/ML-Random%20Forest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

NurseGuard is an AI-powered nurse shift scheduling and fatigue management system designed for hospital administrators. It uses the **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** to generate Pareto-optimal schedules that simultaneously minimize nurse fatigue and staffing constraint violations. A **Random Forest** machine learning model, trained on 31,000+ real nurse schedules, predicts individual burnout risk over the next 30 days.

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Datasets Used](#datasets-used)
- [Fatigue Model — Hospital Regulations](#fatigue-model--hospital-regulations)
- [NSGA-II Algorithm](#nsga-ii-algorithm)
- [Burnout Prediction Model](#burnout-prediction-model)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Dashboard Pages](#dashboard-pages)
- [CSV Format](#csv-format)
- [Future Work](#future-work)
- [References](#references)

---

## Features

- **Role-based login** — Admin, Nurse, and Hospital Manager access levels
- **CSV roster upload** — Upload nurse data with 22 attributes per nurse
- **NSGA-II scheduler** — Multi-objective genetic algorithm optimizing fatigue + constraint violations simultaneously
- **Fatigue scoring** — Real-time fatigue score (0–100) per nurse based on NHS, Joint Commission, and ICN regulations
- **Shift schedule calendar** — Visual weekly calendar with color-coded shifts
- **Constraint violation warnings** — Automatic detection of forbidden shift successions and overwork
- **30-day burnout forecast** — Random Forest model predicting individual burnout risk
- **PDF export** — Download full burnout forecast reports
- **Trained on real data** — Model trained on NSPLib (31,000+ instances), INRC-II, and real hospital benchmark datasets

---

## System Architecture

```
Data Layer
├── INRC-II dataset         → GA scheduler input
├── NSPLib (31,000+ files)  → ML training data
├── Benchmark instances     → ML training data
└── ORTEC XML instances     → ML validation data

Core Engine (Python)
├── parser.py               → Parses INRC-II scenario, demand, history files
├── fatigue_model.py        → Computes fatigue score per nurse (0–100)
└── nsga2.py                → NSGA-II multi-objective genetic algorithm

ML Layer
├── burnout_model.py        → Random Forest trained on all datasets
└── forecast.py             → 30-day burnout risk prediction per nurse

Dashboard (Streamlit)
├── Login page              → Role-based authentication
├── Upload page             → CSV upload + GA trigger + model training
├── Schedule page           → Calendar view + violation warnings
├── Fatigue page            → Score gauges + bar charts
└── Burnout page            → 30-day forecast + PDF export
```

---

## Datasets Used

| Dataset | Source | Size | Role |
|---|---|---|---|
| **INRC-II (n030w4)** | KU Leuven / NRP Competition | 30 nurses, 4 weeks | GA scheduler input |
| **NSPLib** | Ghent University | 31,080 instances | Primary ML training |
| **Scheduling Benchmarks 1–24** | Schedulingbenchmarks.org | 24 real hospital instances | ML training |
| **Scheduling Benchmarks 1–225** | Schedulingbenchmarks.org | 225 instances | ML training |
| **ORTEC instances** | Real hospitals (Netherlands) | 12 XML instances | ML validation |

All datasets are publicly available benchmark datasets used in academic nurse scheduling research.

---

## Fatigue Model — Hospital Regulations

The fatigue score (0–100) is computed using the following real hospital regulations:

### NHS (National Health Service) Guidelines
- Maximum **48 hours per week** — violations add +10 fatigue points per week
- Minimum **11 hours rest** between shifts
- Maximum **12-hour shifts**

### Joint Commission (USA) Standards
- Flag nurses working more than **5 consecutive days** — +5 points per extra day (max 20)
- Flag nurses working more than **3 consecutive night shifts** — +4 points per extra night (max 20)

### ICN (International Council of Nurses) Guidelines
- Weekend work limits
- Night shift penalty — Night shifts carry a base fatigue of 20 points vs 8 for Day shifts

### Forbidden Shift Successions
Based on insufficient rest time between shifts:

| Current Shift | Forbidden Next Shift | Reason |
|---|---|---|
| Night | Early, Day, Late | Less than 11h rest |
| Late | Early | Less than 11h rest |

### Fatigue Score Thresholds

| Score Range | Risk Level | Action |
|---|---|---|
| 0 – 29 | Low (Green) | No action needed |
| 30 – 59 | Moderate (Orange) | Monitor closely |
| 60 – 100 | High Risk (Red) | Immediate schedule adjustment |

---

## NSGA-II Algorithm

NurseGuard uses **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** — the gold standard for multi-objective optimization in nurse scheduling research.

### Two Objectives Optimized Simultaneously

1. **Minimize average fatigue score** across all nurses
2. **Minimize total constraint violations** (understaffing, forbidden successions, overwork)

### Why NSGA-II?

Unlike single-objective GAs, NSGA-II produces a **Pareto front** — a set of optimal solutions where improving one objective cannot be done without worsening the other. This gives the admin flexibility to choose a schedule based on their priorities.

### Algorithm Parameters

| Parameter | Default | Description |
|---|---|---|
| Population size | 30 | Number of schedules per generation |
| Generations | 50 | Number of evolution iterations |
| Mutation rate | 0.02 | Probability of random shift change |
| Crossover | Single-point | Swap nurse assignments at random point |
| Selection | Tournament | Rank-based tournament selection |

### Chromosome Encoding

Each individual in the population is a dictionary:
```
{nurse_id: [shift_day_1, shift_day_2, ..., shift_day_28]}
```
Where each shift is one of: `Early`, `Day`, `Late`, `Night`, `Off`

---

## Burnout Prediction Model

### Model: Random Forest Regressor

Trained on features extracted from 31,000+ nurse schedules across NSPLib and benchmark datasets.

### Input Features (8 features per nurse)

| Feature | Description |
|---|---|
| Night shift ratio | Proportion of nights out of total days |
| Late shift ratio | Proportion of late shifts |
| Days off ratio | Proportion of rest days |
| Early shift ratio | Proportion of early shifts |
| Max consecutive work streak | Longest working streak in days |
| Weekend work count | Number of weekend days worked |
| Bad transitions | Night → Early/Day transitions (insufficient rest) |
| Fatigue load | Weighted fatigue across all shifts |

### Training

```
Total training samples: ~15,000+
Train/test split: 80/20
Model: RandomForestRegressor(n_estimators=200, max_depth=10)
Validation: ORTEC XML instances (unseen real hospital data)
```

### Output

A burnout risk percentage (0–100%) per nurse for the next 30 days, with a projected trend line showing risk trajectory.

---

## Project Structure

```
nurse_fatigue_system/
│
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── data/
│   ├── inrc2/                      # INRC-II dataset (Sc, WD, H0 files)
│   ├── nsplib/                     # NSPLib benchmark instances
│   ├── benchmarks/
│   │   ├── instances1_24/          # 24 real hospital instances
│   │   └── instances1_225/         # 225 larger instances
│   └── validation/                 # ORTEC XML validation instances
│
├── engine/
│   ├── __init__.py
│   ├── parser.py                   # INRC-II file parser
│   ├── fatigue_model.py            # Fatigue scoring engine
│   └── nsga2.py                    # NSGA-II genetic algorithm
│
├── ml/
│   ├── __init__.py
│   ├── burnout_model.py            # Random Forest training + prediction
│   ├── burnout_rf.pkl              # Saved trained model (generated)
│   └── burnout_scaler.pkl          # Saved scaler (generated)
│
└── pages/
    ├── __init__.py
    ├── login.py                    # Authentication page
    ├── upload.py                   # CSV upload + GA scheduler
    ├── schedule.py                 # Calendar view + violations
    ├── fatigue.py                  # Fatigue scores + gauges
    └── burnout.py                  # 30-day forecast + PDF export
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Git
- VS Code (recommended)

### Step 1 — Clone the repository

```bash
git clone https://github.com/Malik8122/nurse-fatigue-scheduler.git
cd nurse-fatigue-scheduler
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Verify dataset files

Make sure the following files exist:
```
data/inrc2/Sc-n030w4.txt
data/inrc2/WD-n030w4-0.txt
data/inrc2/H0-n030w4-0.txt
data/nsplib/          ← NSPLib .nsp files
data/benchmarks/      ← benchmark .txt files
data/validation/      ← ORTEC .xml files
```

---

## Running the App

```bash
streamlit run app.py
```

Or if streamlit is not in PATH:

```bash
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Dashboard Pages

### Login
Role-based authentication with three access levels:

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | All pages |
| Nurse | `nurse1` | `nurse123` | Fatigue + Burnout only |
| Manager | `manager` | `manager123` | All pages |

### Upload & Schedule
1. View dataset training status (NSPLib, benchmark, validation file counts)
2. Train the burnout model on all datasets (one-time, ~1-2 mins)
3. Upload nurse roster CSV (800 sample nurses included)
4. Configure GA parameters (generations, population size)
5. Click **Generate Optimal Schedule** to run NSGA-II

### Schedule View
- Color-coded shift calendar (Early=Blue, Day=Green, Late=Amber, Night=Purple, Off=Gray)
- Shift distribution bar chart
- Automatic constraint violation detection and warnings

### Fatigue Scores
- Summary metrics (High/Moderate/Low risk counts)
- Bar chart with NHS regulation threshold lines
- Individual nurse fatigue gauge (0–100)

### Burnout Forecast
- 30-day burnout risk prediction per nurse
- Top 5 at-risk nurse trend lines
- Automated recommendations for high-risk nurses
- Export full report as PDF

---

## CSV Format

Upload a CSV with the following columns:

| Column | Description | Example |
|---|---|---|
| nurse_id | Unique ID | HN_001 |
| name | Full name | Priya Sharma |
| age | Age in years | 34 |
| gender | Male/Female | Female |
| skill | HeadNurse/Nurse/Caretaker/Trainee | Nurse |
| contract | FullTime/PartTime/HalfTime | FullTime |
| experience_level | Junior/Mid/Senior | Mid |
| years_experience | Years of experience | 5 |
| department | Hospital department | ICU |
| preferred_shift | Early/Day/Late/Night | Day |
| max_nights_per_week | Max night shifts per week | 3 |
| max_consecutive_days | Max days worked in a row | 5 |
| min_rest_hours | Minimum rest between shifts | 11 |
| max_weekly_hours | Maximum hours per week | 48 |
| current_fatigue_score | Current fatigue level (0–100) | 45 |
| on_leave | Yes/No | No |

A sample roster of 800 nurses is included at `data/nurse_roster.csv`.

---

## Future Work

- [ ] React + Figma frontend replacing Streamlit
- [ ] FastAPI backend for REST API access
- [ ] Real-time nurse mobile app (shift notifications)
- [ ] Integration with hospital HR systems
- [ ] Deep learning burnout model (LSTM for time-series fatigue)
- [ ] Multi-department scheduling across entire hospital
- [ ] Automated shift swap recommendations
- [ ] WhatsApp/email alerts for high-risk nurses

---

## References

1. Maenhout, B. and Vanhoucke, M. (2008). "Comparison and Hybridization of Crossover Operators for the Nurse Scheduling Problem." *Annals of Operations Research*, 159, 333–353.
2. Deb, K., Pratap, A., Agarwal, S., and Meyarivan, T. (2002). "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II." *IEEE Transactions on Evolutionary Computation*, 6(2), 182–197.
3. Ceschia, S. et al. (2019). "Second International Nurse Rostering Competition (INRC-II)." *Annals of Operations Research*.
4. NHS (2023). "Working Hours and Rest Breaks." *NHS Employers Guidance*.
5. Joint Commission (2022). "Nurse Fatigue and Patient Safety." *Joint Commission Resources*.
6. ICN (2021). "Nurse Staffing and Patient Outcomes." *International Council of Nurses*.

---

## License

MIT License — free to use for academic and research purposes.

---

## Author

Developed as part of a final year project on intelligent healthcare scheduling systems.  
GitHub: [@Malik8122](https://github.com/Malik8122)
