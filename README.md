# Car Showroom Lead Intelligence System – Indore

## Overview

The Car Showroom Lead Intelligence System is a data-driven project developed to identify potential business leads among car showrooms in Indore. The system automatically gathers showroom information, analyzes their online presence, extracts contact details, and categorizes businesses based on lead potential.

The objective of the project is to help sales and marketing teams identify businesses that may benefit from digital services by highlighting showrooms with limited online visibility.

This project was developed during a Data Science Internship at Positiveway Solutions Pvt Ltd.

---

## Project Workflow

The system follows a multi-step pipeline:

1. Collects car showroom data from OpenStreetMap.
2. Searches for each showroom online using DuckDuckGo Search.
3. Checks whether the showroom has an official website or relies mainly on referral platforms.
4. Extracts phone numbers using automated web searches.
5. Assigns a lead score based on online presence.
6. Displays the results through an interactive Streamlit dashboard.

---

## Lead Classification

Businesses are categorized according to their online presence and opportunity potential.

* Hot Lead: Businesses with little or no online presence and no official website.
* High Priority: Businesses with limited digital visibility and few referral listings.
* Medium Priority: Businesses with some online presence but room for improvement.
* Low Priority: Businesses that already have a website but still show minor gaps.
* Strong Online Presence: Businesses that are already well-established online.

---

## Technologies Used

The project was built using the following technologies:

* Python
* OpenStreetMap (Overpy)
* DuckDuckGo Search (DDGS)
* Selenium
* ChromeDriver
* Pandas
* Streamlit

---

## Project Structure

```text
lead_gen_project/
│
├── osm_scraper.py
├── online_presence_checker.py
├── scorer.py
├── google_phone_scraper.py
├── merge_final.py
├── app.py
└── requirements.txt
```

Each script performs a specific task in the lead generation pipeline, from data collection to dashboard visualization.

---

## Running the Project

### Clone the Repository

```bash
git clone https://github.com/YOURUSERNAME/car-showroom-lead-intelligence.git
cd car-showroom-lead-intelligence
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Execute the Data Pipeline

```bash
python osm_scraper.py
python online_presence_checker.py
python scorer.py
python google_phone_scraper.py --input car_showroom_leads_scored.csv --name-column name
python merge_final.py
```

### Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will be available locally in your browser.

---

## Dashboard Features

The Streamlit dashboard provides:

* Summary statistics for total businesses and lead categories
* Search functionality for finding specific showrooms
* Category-based filtering
* Website and phone number availability indicators
* Detailed lead information cards
* Raw data viewing option
* CSV export functionality

---

## Dependencies

Required Python libraries include:

```text
overpy
pandas
ddgs
selenium
webdriver-manager
requests
streamlit
```

## Author

Shivansh

Data Science Intern
Positiveway Solutions Pvt Ltd

Bsc Data Science
SUAS, Indore

This project was developed for learning and internship purposes as part of practical training in Data Science and Business Intelligence.
