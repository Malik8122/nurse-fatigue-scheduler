Design a modern, dark-theme dashboard UI for a Hospital Staff Shift Scheduling System powered by a Genetic Algorithm (NSGA-II) with fatigue constraints.

The interface should look like a professional AI-powered healthcare analytics platform, combining elements of hospital management and data science dashboards.

Overall layout:

* Use a desktop frame (1440x1024)
* Left sidebar navigation (fixed width ~240px)
* Main content area on the right with structured sections
* Use clean spacing, grid alignment, and auto-layout

Color theme:

* Background: deep navy/black (#0B1220)
* Cards: slightly lighter dark (#111827)
* Primary accent: red (#EF4444)
* Success: green (#22C55E)
* Text: light gray/white (#E5E7EB)

Typography:

* Font: Inter or Poppins
* Headings: bold, large (28–36px)
* Subheadings: medium (18–22px)
* Body: regular (14–16px)

---

## SIDEBAR (LEFT PANEL)

* App title: "Hospital Scheduler AI"
* Menu items with icons:

  * Upload & Schedule
  * Schedule View
  * Fatigue Scores
  * Burnout Forecast
* Highlight active tab
* Bottom section:

  * Logged in user (Admin)
  * Logout button

---

## SCREEN 1: DATA UPLOAD & MODEL STATUS

Top heading:
"Upload Nurse Data & Generate Schedule"

Section 1: Dataset Status Cards (4 cards in a row)

* NSPLib Files count
* Benchmark-24
* Benchmark-225
* Validation Set
  Each card:
* Rounded corners (12px)
* Subtle shadow
* Large numeric value + small label

Section 2: Model Status Banner

* Green success banner:
  "Burnout model is trained and ready"
* Include subtle icon (checkmark)

Section 3: Upload Area

* Drag-and-drop file upload box
* Dashed border
* Icon + text:
  "Drag and drop CSV file"
* Secondary button: "Browse Files"

---

## SCREEN 2: GA OPTIMIZATION PANEL

Title:
"Generate Optimal Schedule via NSGA-II"

Controls:

* Slider: Generations
* Slider: Population Size
* Show numeric value above sliders

Primary Button:

* Large CTA button:
  "Generate Optimal Schedule"

After run (results state):

* Success banner: "Schedule generated successfully"

Metrics Cards (3 cards):

* Avg Fatigue Score (e.g., 37.9/100)
* High Risk Nurses (count)
* Nurses Scheduled (count)

---

## SCREEN 3: SCHEDULE VIEW

Title:
"Shift Schedule Calendar"

Top Filter Section:

* Filter chips (rounded pills)
* Nurse IDs (HN_0, NU_1, etc.)
* Active filters in red

Main Table:

* Large grid table
* Columns: Nurse + Days (W1-Mon, W1-Tue, etc.)
* Cell values: Early / Late / Night / Off
* Alternate row shading

Section: Shift Distribution

* Bar chart
* Categories:
  Off, Late, Day, Early, Night

Section: Constraint Violations

* Table with columns:
  Nurse | Issue | Day
* Example issue:
  "Night → Early shift violation"

---

## SCREEN 4: FATIGUE ANALYTICS

Title:
"Nurse Fatigue Scores"

Top Summary Cards:

* High Risk (60–100)
* Moderate Risk (30–60)
* Low Risk (0–30)

Main Chart:

* Bar chart: fatigue score per nurse
* Add horizontal threshold lines:

  * Red line (High risk threshold)
  * Yellow line (Moderate threshold)

Legend:

* Color-coded risk levels

---

## DESIGN STYLE

* Minimal, modern, clean
* Use soft shadows and rounded cards
* Maintain consistent spacing (8pt grid system)
* Use auto layout for responsiveness
* Keep UI slightly futuristic (AI-powered feel)

---

## INTERACTIONS (OPTIONAL)

* Hover states for buttons
* Active states for sidebar
* Loading indicator when generating schedule

The final design should feel like a professional AI decision-support system used by hospital administrators for workforce optimization and fatigue management.
