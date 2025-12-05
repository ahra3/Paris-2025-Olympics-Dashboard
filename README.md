# 🏅 Olympic Data Analytics Dashboard

An interactive Streamlit dashboard that transforms Olympic datasets into dynamic, visual, and insightful analytics.  
Users can explore athletes, countries, sports, events, and medal performance through interactive charts, filters, and drill-down analysis pages.

This dashboard emphasizes clarity, speed, and a smooth analytical workflow for students, analysts, and sports enthusiasts.

---

# 📄 Dashboard Pages & Features

Below is a detailed breakdown of each dashboard page, including objectives, key features, and creative contributions.

---

## 🏠 Page 1 — Overview (The Command Center)

### **Objective**

Provide an immediate, reactive summary of the most essential Olympic statistics.

### **Features**

| Component                                 | Description                                                                                   | Status       |
| ----------------------------------------- | --------------------------------------------------------------------------------------------- | ------------ |
| **KPI Metrics Section (5 indicators)**    | Displays Total Athletes, Countries, Sports, Medals, and Events — fully responsive to filters. | ✔️ Completed |
| **Global Medal Distribution (Pie Chart)** | Visual breakdown of Gold/Silver/Bronze medals.                                                | ✔️ Completed |
| **Top 10 Medal Standings (Bar Chart)**    | Horizontal bar chart showing the top 10 performing countries.                                 | ✔️ Completed |

### **Creative Contribution — Athlete Detailed Profile (Originally part of Page 3)**

A dynamic **Athlete Profile Card** has been added directly on the home page.

**Advantages:**

- Enhances user experience by enabling quick athlete lookup without page switching.
- Consolidates critical information in one central "Command Center."

**Implementation Details:**

- User selects an athlete from a filter-based dropdown.
- The profile displays:
  - Name, Country, Gender
  - Disciplines & Events
  - Personal Medal Count (Gold, Silver, Bronze)
- Built using merged datasets and dynamic filtering logic.

---


## 🗺️ Page 2 — Global Analysis (Worldwide Insights)

### **Objective**

Provide a global, high-level analytical view of Olympic performance across countries, continents, and medal structures.



## **Features**

The Global Analysis page is structured into multiple interactive tabs, each offering a unique perspective on worldwide Olympic results.

### 🌍 **1. World Medal Map**

- Choropleth world map showing total medals per country
- Color-coded intensity highlights performance dominance
- Fully reactive to filters (year, sport, gender, etc.)

### 🥇 **2. Medal Hierarchy (Sunburst Chart)**

- Hierarchical visualization of **Medals → Continents → Countries**
- Shows how medals are distributed across geographical layers
- Reveals which continents contribute the most to global totals

### 🌎 **3. Continent Comparison**

- Side-by-side continent-level medal analytics
- Bar/stacked charts showing Gold/Silver/Bronze counts
- Helps identify disparities and regional strengths

### 🏆 **4. Top 20 Countries**

- Ranked bar chart of the top 20 medal-winning nations
- Also displays total medals and podium breakdown
- Ideal for quick identification of global leaders



## **Creative Contribution**

### 👥 **5. Medals by Gender**

- Visual comparison of **Male vs Female** medal distribution
- Can be filtered by sport, region, or event type
- Useful for gender-based performance studies

### 🥉 **6. Top 10 Sports — Custom Medal Ranking**

A custom visualization ranking the **Top 10 Sports** based on total medal count.  
**Why it’s valuable:**

- Highlights the most competitive and medal-dense sports
- Helps understand which disciplines dominate the Olympic landscape
- Fully dynamic with filters applied



---

## 👤 Page 3 — Athlete Performance (Athlete Insights Hub)

### **Objective**

Provide detailed, athlete-centric analysis covering demographics, medal achievements, gender patterns, and country comparisons.

### **Features**

### 🔹 Athlete Profile Viewer

View full information for any athlete, including:

- Country + Flag
- Age, Height, Weight
- Coach
- Disciplines & Events

### 🔹 Athlete Age Distribution

- Violin plots grouped by **Gender**, **Sport**, and **Country**
- Includes summary statistics table

### 🔹 Gender Distribution

- Global, continental, and national-level views
- Pie charts + bar charts

### 🔹 Top Athletes by Medals

- Interactive slider to select Top N medalists
- Bar chart + summary table

### 🔹 Country Performance Analysis

Compare countries based on:

- Total medals
- Gold medals
- Male medals
- Female medals

### 🔹 Medal Distributions

- Choropleth world map for medal visualization
- Medal distribution per continent

### 🔹 Country vs Country Comparison

A head-to-head comparison of two selected nations on all medal types.

---

## 🏟️ Page 4 — Sports & Events (The Competition Arena)

### **Objective**

Analyze Olympic events from the perspective of scheduling, medal distribution by sport, and venue usage.

### **Features**

| Component                                 | Description                                                                      | Status       |
| ----------------------------------------- | -------------------------------------------------------------------------------- | ------------ |
| **Event Schedule (Timeline/Gantt Chart)** | Shows the timeline of events for any selected sport.                             | ✔️ Completed |
| **Medal Count by Sport (Treemap)**        | Hierarchical Treemap: Total Medals → Sport → Country, fully reactive to filters. | ✔️ Completed |
| **Venue Map (Scatter Mapbox)**            | Replaced with Venue Usage Analysis due to missing coordinates.                   | ⚠️ Modified  |

### **Creative Contribution — Venue Usage Intensity Analysis**

The original Venue Map requirement could not be implemented since _venues.csv_ did not contain latitude/longitude data.

It has been replaced with a more meaningful analytical feature:

#### **Venue Usage Intensity (Bar Chart)**

A visualization of the **Total Duration (in days)** of events hosted at each venue.

**Advantages:**

- Provides actionable insights for future logistical planning.
- Highlights the most heavily used venues during the competition.

**Implementation:**

- Duration is calculated using each event's `start_date` and `end_date` from _schedule.csv_.
- Aggregated per venue and visualized in a bar chart.

---

# 📁 Project Structure

📦 Olympic-Dashboard
│
├── data/
├── pages/
├── utils/
│
├── .gitignore
├── README.md
├── 🏠_Home.py
├── requirements.txt

---

# 🛠️ How to Run the Project Locally

### **1️⃣ Clone the repository**

```bash
git clone <your-repo-url>
cd <project-folder>
```

### **2️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Launch the Streamlit application**

```bash
streamlit run 🏠_Home.py
```

### **4️⃣ The dashboard will open in your browser at:**

http://localhost:8501

# 🎥 Demonstration Video:
    👉 https://drive.google.com/file/d/1vZSddgtS8MKUp6T6FYa_PFP1CWAcN2Kd/view?usp=sharing

 

# 🚀 Live Deployment :
   👉 https://paris-2025-olympics-dashboard.streamlit.app

 

# 🙌 Acknowledgements

This dashboard was collaboratively created as part of an Olympic data analysis project, combining analytics, design, and interactive visualization.
