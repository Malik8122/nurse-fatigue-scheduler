# ml/burnout_model.py
import numpy as np
import os
import glob
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

MODEL_PATH  = "ml/burnout_rf.pkl"
SCALER_PATH = "ml/burnout_scaler.pkl"

SHIFT_MAP = {1: "Early", 2: "Day", 3: "Late", 4: "Night", 0: "Off"}
SHIFT_FATIGUE = {"Early": 10, "Day": 8, "Late": 12, "Night": 20, "Off": 0}
FORBIDDEN = {"Night": ["Early","Day"], "Late": ["Early"], "Day": [], "Early": [], "Off": []}

# ─── PARSERS ───────────────────────────────────────────────

def parse_nsp_file(filepath):
    """Parse NSPLib .nsp file → list of nurse shift sequences"""
    schedules = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            return schedules
        header = lines[0].split()
        num_nurses = int(header[0])
        # Nurse schedule starts after header + demand block
        # Each nurse row = tab-separated shift numbers
        nurse_lines = []
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) >= 7:
                nurse_lines.append(parts)
        for row in nurse_lines[:num_nurses]:
            shifts = []
            for val in row:
                val = val.strip()
                if val.isdigit():
                    shifts.append(SHIFT_MAP.get(int(val), "Off"))
            if len(shifts) >= 7:
                schedules.append(shifts)
    except Exception:
        pass
    return schedules


def parse_benchmark_txt(filepath):
    """Parse instances1_24 / instances1_225 .txt files → nurse shift sequences"""
    schedules = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()
        # Extract staff constraints for feature building
        staff_lines = []
        in_staff = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if line == "SECTION_STAFF":
                in_staff = True
                continue
            if line.startswith("SECTION_") and in_staff:
                break
            if in_staff:
                staff_lines.append(line)
        # Extract cover requirements → infer shift pattern per nurse
        cover = []
        in_cover = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if line == "SECTION_COVER":
                in_cover = True
                continue
            if line.startswith("SECTION_") and in_cover:
                break
            if in_cover:
                parts = line.split(",")
                if len(parts) >= 3:
                    cover.append(int(parts[2]) if parts[2].strip().isdigit() else 0)
        # Build synthetic nurse schedules from staff constraints
        for staff in staff_lines:
            parts = staff.split(",")
            if len(parts) < 7:
                continue
            try:
                max_consec = int(parts[4])
                min_consec = int(parts[5])
                min_days_off = int(parts[6])
                # Simulate a 14-day schedule based on constraints
                schedule = []
                work_streak = 0
                off_streak = 0
                for d in range(14):
                    if work_streak >= max_consec:
                        schedule.append("Off")
                        work_streak = 0
                        off_streak += 1
                    elif off_streak >= min_days_off and work_streak < min_consec:
                        schedule.append("Day")
                        work_streak += 1
                        off_streak = 0
                    elif work_streak >= min_consec and d % 7 in [5, 6]:
                        schedule.append("Off")
                        work_streak = 0
                        off_streak += 1
                    else:
                        schedule.append("Day")
                        work_streak += 1
                        off_streak = 0
                schedules.append(schedule)
            except Exception:
                continue
    except Exception:
        pass
    return schedules


# ─── FEATURE EXTRACTION ────────────────────────────────────

def extract_features_from_shifts(shifts):
    """Extract 8 fatigue features from a shift sequence"""
    total = len(shifts)
    if total == 0:
        return None

    nights    = shifts.count("Night") / total
    lates     = shifts.count("Late")  / total
    days_off  = shifts.count("Off")   / total
    early     = shifts.count("Early") / total

    # Longest consecutive work streak
    max_streak = streak = 0
    for s in shifts:
        streak = streak + 1 if s != "Off" else 0
        max_streak = max(max_streak, streak)

    # Weekend work count
    weekends = sum(1 for i, s in enumerate(shifts) if i % 7 in [5,6] and s != "Off")

    # Bad transitions (Night → Early/Day)
    bad_trans = sum(1 for i in range(len(shifts)-1)
                    if shifts[i] == "Night" and shifts[i+1] in ["Early","Day"])

    # Base fatigue load
    fatigue_load = sum(SHIFT_FATIGUE.get(s, 0) for s in shifts) / (total * 20)

    return [nights, lates, days_off, early, max_streak, weekends, bad_trans, fatigue_load]


def compute_fatigue_label(shifts):
    """Rule-based fatigue score used as training label"""
    from engine.fatigue_model import compute_fatigue_score
    return compute_fatigue_score(shifts)


# ─── TRAINING ──────────────────────────────────────────────

def build_training_data():
    """Load all datasets and build X, y for training"""
    X, y = [], []

    # 1. NSPLib — thousands of .nsp files
    nsp_files = glob.glob("data/nsplib/**/*.nsp", recursive=True)
    print(f"Found {len(nsp_files)} NSPLib files...")
    for fp in nsp_files[:500]:  # cap at 500 for speed
        for shifts in parse_nsp_file(fp):
            feats = extract_features_from_shifts(shifts)
            if feats:
                X.append(feats)
                y.append(compute_fatigue_label(shifts))

    # 2. Benchmarks instances1_24
    bench24_files = glob.glob("data/benchmarks/instances1_24/**/*.txt", recursive=True)
    print(f"Found {len(bench24_files)} benchmark-24 files...")
    for fp in bench24_files:
        for shifts in parse_benchmark_txt(fp):
            feats = extract_features_from_shifts(shifts)
            if feats:
                X.append(feats)
                y.append(compute_fatigue_label(shifts))

    # 3. Benchmarks instances1_225
    bench225_files = glob.glob("data/benchmarks/instances1_225/**/*.txt", recursive=True)
    print(f"Found {len(bench225_files)} benchmark-225 files...")
    for fp in bench225_files:
        for shifts in parse_benchmark_txt(fp):
            feats = extract_features_from_shifts(shifts)
            if feats:
                X.append(feats)
                y.append(compute_fatigue_label(shifts))

    print(f"Total training samples: {len(X)}")
    return np.array(X), np.array(y)


def train_burnout_model():
    """Train Random Forest on all datasets and save model"""
    print("Building training data from all datasets...")
    X, y = build_training_data()

    if len(X) < 10:
        print("Not enough training data found. Check your data folders.")
        return None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train_sc, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test_sc))
    print(f"Model trained. MAE on test set: {mae:.2f} fatigue points")

    os.makedirs("ml", exist_ok=True)
    with open(MODEL_PATH,  "wb") as f: pickle.dump(model,  f)
    with open(SCALER_PATH, "wb") as f: pickle.dump(scaler, f)
    print("Model saved to ml/burnout_rf.pkl")
    return model, scaler


# ─── PREDICTION ────────────────────────────────────────────

def predict_burnout_30days(schedule_dict):
    """Predict burnout risk per nurse for next 30 days"""
    if not os.path.exists(MODEL_PATH):
        print("No trained model found. Training now...")
        train_burnout_model()

    if not os.path.exists(MODEL_PATH):
        return {nid: 50.0 for nid in schedule_dict}

    with open(MODEL_PATH,  "rb") as f: model  = pickle.load(f)
    with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)

    results = {}
    for nid, shifts in schedule_dict.items():
        feats = extract_features_from_shifts(shifts)
        if feats:
            X = scaler.transform([feats])
            results[nid] = round(float(model.predict(X)[0]), 1)
        else:
            results[nid] = 50.0
    return results


def get_model_stats():
    """Return model training stats for dashboard display"""
    nsp_count   = len(glob.glob("data/nsplib/**/*.nsp",   recursive=True))
    b24_count   = len(glob.glob("data/benchmarks/instances1_24/**/*.txt",  recursive=True))
    b225_count  = len(glob.glob("data/benchmarks/instances1_225/**/*.txt", recursive=True))
    ortec_count = len(glob.glob("data/validation/*.xml"))
    return {
        "nsplib_files":    nsp_count,
        "benchmark24":     b24_count,
        "benchmark225":    b225_count,
        "validation_files": ortec_count,
        "model_trained":   os.path.exists(MODEL_PATH)
    }