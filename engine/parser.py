# engine/parser.py
import re
import os

def parse_scenario(filepath):
    scenario = {
        "name": "", "weeks": 0, "skills": [],
        "shift_types": {}, "forbidden_successions": {},
        "contracts": {}, "nurses": {}
    }
    with open(filepath) as f:
        lines = [l.strip() for l in f if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("SCENARIO"):
            scenario["name"] = line.split("=")[1].strip()
        elif line.startswith("WEEKS"):
            scenario["weeks"] = int(line.split("=")[1].strip())
        elif re.match(r"SKILLS\s*=", line):
            count = int(re.split(r"=", line)[1].strip())
            for j in range(count):
                scenario["skills"].append(lines[i + 1 + j])
            i += count
        elif re.match(r"SHIFT_TYPES\s*=", line):
            count = int(re.split(r"=", line)[1].strip())
            for j in range(count):
                raw = lines[i + 1 + j]
                nums = re.findall(r'\d+', raw)
                name = raw.split()[0]
                scenario["shift_types"][name] = {"min": int(nums[0]), "max": int(nums[1])}
            i += count
        elif line.startswith("FORBIDDEN_SHIFT_TYPES_SUCCESSIONS"):
            shift_names = list(scenario["shift_types"].keys())
            for j in range(len(shift_names)):
                parts = lines[i + 1 + j].split()
                shift = parts[0]
                count_f = int(parts[1])
                scenario["forbidden_successions"][shift] = parts[2:2 + count_f]
            i += len(shift_names)
        elif re.match(r"CONTRACTS\s*=", line):
            count = int(re.split(r"=", line)[1].strip())
            for j in range(count):
                raw = lines[i + 1 + j]
                name = raw.split()[0]
                nums = re.findall(r'\d+', raw)
                scenario["contracts"][name] = {
                    "min_shifts":      int(nums[0]),
                    "max_shifts":      int(nums[1]),
                    "min_consec_work": int(nums[2]),
                    "max_consec_work": int(nums[3]),
                    "min_consec_off":  int(nums[4]),
                    "max_consec_off":  int(nums[5]),
                    "max_weekends":    int(nums[6]) if len(nums) > 6 else 2
                }
            i += count
        elif re.match(r"NURSES\s*=", line):
            count = int(re.split(r"=", line)[1].strip())
            for j in range(count):
                parts = lines[i + 1 + j].split()
                nurse_id = parts[0]
                contract = parts[1]
                num_skills = int(parts[2])
                skills = parts[3:3 + num_skills]
                scenario["nurses"][nurse_id] = {"contract": contract, "skills": skills}
            i += count
        i += 1
    return scenario


def parse_week_demand(filepath):
    demands, off_requests = {}, []
    DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    with open(filepath) as f:
        lines = [l.strip() for l in f if l.strip()]
    i = 0
    while i < len(lines):
        if lines[i] == "REQUIREMENTS":
            i += 1
            while i < len(lines) and not lines[i].startswith("SHIFT_OFF"):
                parts = lines[i].split()
                if len(parts) >= 9:
                    shift, skill = parts[0], parts[1]
                    day_reqs = []
                    for d in range(7):
                        pair = parts[2 + d].strip("()")
                        mn, mx = pair.split(",")
                        day_reqs.append((int(mn), int(mx)))
                    demands.setdefault(shift, {})[skill] = day_reqs
                i += 1
        elif lines[i].startswith("SHIFT_OFF_REQUESTS"):
            count = int(lines[i].split("=")[1].strip())
            for j in range(count):
                p = lines[i + 1 + j].split()
                if len(p) >= 3:
                    off_requests.append({
                        "nurse": p[0],
                        "shift": p[1],
                        "day": DAYS.index(p[2]) if p[2] in DAYS else 0
                    })
            i += count
        i += 1
    return {"demands": demands, "off_requests": off_requests}


def parse_history(filepath):
    history = {}
    try:
        with open(filepath) as f:
            lines = [l.strip() for l in f if l.strip()]
        for line in lines:
            if line.startswith("HISTORY") or line.startswith("n0"):
                continue
            parts = line.split()
            if len(parts) >= 3:
                history[parts[0]] = {
                    "last_shift": parts[1],
                    "consec_work": int(parts[2]),
                    "consec_off": int(parts[3]) if len(parts) > 3 else 0
                }
    except Exception:
        pass
    return history


def load_all(data_dir, scenario_file, week_demand_files, history_file):
    sc = parse_scenario(os.path.join(data_dir, scenario_file))
    weeks = []
    for wf in week_demand_files:
        fp = os.path.join(data_dir, wf)
        if os.path.exists(fp):
            weeks.append(parse_week_demand(fp))
    if not weeks:
        weeks = [{"demands": {}, "off_requests": []}]
    hist = parse_history(os.path.join(data_dir, history_file))
    return sc, weeks, hist
