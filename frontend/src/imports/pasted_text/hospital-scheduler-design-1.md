Design a professional hospital management dashboard UI for an AI-powered Nurse Scheduling and Fatigue Monitoring System.

The design should resemble real hospital software (like Epic Systems or NHS dashboards), not a generic tech dashboard. It must feel clean, trustworthy, clinical, and data-driven.

---

## OVERALL LAYOUT

* Desktop frame: 1440 × 1024
* Layout: left sidebar + main content area
* Use grid-based alignment and consistent spacing (8px system)
* Minimal clutter, high readability

---

## COLOR STYLE (HOSPITAL THEME)

* Background: #F8FAFC (light clinical)
* Cards: #FFFFFF (clean white)
* Primary: #2563EB (medical blue)
* Secondary: #0EA5E9
* Success: #16A34A
* Danger: #DC2626
* Text: #1E293B (dark gray)

---

## TYPOGRAPHY

* Font: Inter or Poppins
* Headings: 28–36 px, bold
* Subheadings: 18–22 px
* Body text: 14–16 px
* Clean, readable, hospital-grade typography

---

## SCREEN 1: LOGIN PAGE

Design a clean login screen centered on the page.

Layout:

* Hospital logo or icon at top
* Title: "Hospital Scheduler AI"
* Subtitle: "AI-powered Workforce Optimization System"

Login card:

* White card with soft shadow and rounded corners (12px)
* Fields:

  * Username input
  * Password input
* Primary button: "Login"
* Secondary text: "Admin / Nurse / Manager access"

Optional:

* Subtle medical illustration or background gradient
* Trust elements like "Secure Login" or "HIPAA compliant style"

---

## SIDEBAR (LEFT NAVIGATION)

* Dark blue sidebar (#1E3A8A)

* Logo/title at top:
  "Hospital Scheduler AI"

* Menu items with icons:

  * Upload & Schedule
  * Schedule View
  * Fatigue Scores
  * Burnout Forecast

* Highlight active page with background

* Bottom section:

  * User profile (Admin)
  * Email or role
  * Logout button

---

## SCREEN 2: DASHBOARD (UPLOAD & SYSTEM STATUS)

Header:
"Upload Nurse Data & Generate Schedule"

Section 1: Metrics Cards (4 cards)

* NSPLib Files
* Benchmark-24
* Benchmark-225
* Validation Set

Each card:

* White background
* Rounded corners
* Soft shadow
* Large number + small label

Section 2: Status Banner

* Green success banner:
  "Burnout model is trained and ready"

Section 3: Upload Panel

* Drag-and-drop box with dashed border
* Icon + text: "Upload nurse roster CSV"
* Button: "Browse Files"

---

## SCREEN 3: GA OPTIMIZATION PANEL

Title:
"Generate Optimal Schedule (NSGA-II)"

Controls:

* Slider: Generations
* Slider: Population Size
* Show values dynamically

Primary button:
"Generate Optimal Schedule"

After action:

* Success banner
* Smooth transition to results

Metrics:

* Avg Fatigue Score
* High Risk Nurses
* Nurses Scheduled

---

## SCREEN 4: SCHEDULE VIEW

Title:
"Shift Schedule Calendar"

Top:

* Filter chips for nurses (HN_0, NU_1, etc.)

Main:

* Table grid:
  Nurse vs Days
  Values:
  Early, Day, Late, Night, Off

Below:

* Shift Distribution bar chart
* Constraint Violations table:
  Nurse | Issue | Day

---

## SCREEN 5: FATIGUE ANALYTICS

Title:
"Nurse Fatigue Scores"

Top cards:

* High Risk
* Moderate Risk
* Low Risk

Main visualization:

* Bar chart per nurse
* Add threshold lines:

  * Red line (High risk)
  * Yellow line (Moderate)

Legend:

* Risk categories

---

## DESIGN STYLE

* Clean hospital aesthetic
* Minimal and professional
* Avoid flashy neon colors
* Use white space effectively
* Soft shadows and rounded components
* High contrast for readability

---

## INTERACTIONS (OPTIONAL)

* Hover effects on buttons
* Active sidebar highlight
* Loading spinner when generating schedule
* Smooth transitions between sections

---

## GOAL

The final design should feel like a real hospital decision-support system used by administrators to manage staff scheduling, reduce fatigue, and improve patient safety using AI.
