# E-Commerce Funnel Analysis

A complete funnel analysis project simulating 50,000 user sessions through an e-commerce purchase funnel. Identifies drop-off points, conversion bottlenecks, and revenue opportunities across device types, traffic sources, geographies, and time patterns.

## Key Questions Answered

- Where exactly are users dropping off in the purchase funnel?
- Which device converts best — mobile, desktop, or tablet?
- Which traffic source brings the highest quality users?
- Which countries have the best and worst conversion rates?
- What time of day and day of week drives most conversions?
- Which product categories generate the most revenue?

## Insights Discovered

- Overall conversion rate across all 50,000 sessions
- Biggest drop-off stage identified with actionable recommendations
- Email traffic converts significantly better than paid ads
- Desktop users convert at higher rates despite mobile having more traffic
- Clear peak conversion hours identified for ad spend optimization

## Tech Stack

- **Python** — Pandas, NumPy, Matplotlib
- **Data** — Synthetic dataset generated with realistic business logic
- **Visualizations** — 6 multi-panel analysis charts (24 individual plots)

## Setup

1. Clone the repo
2. `python -m venv venv` then activate
3. `pip install -r requirements.txt`
4. `python analysis.py` (generates data + charts automatically)
5. Charts saved to `outputs/` folder

## Charts Generated

1. **Main Funnel** — User counts and drop-off rates at each stage
2. **Device Analysis** — Conversion, funnel progression, revenue by device
3. **Traffic Source** — Conversion rates and revenue by acquisition channel
4. **Geography** — Country-level conversion and revenue breakdown
5. **Time & Category** — Hourly, daily, monthly patterns + category performance
6. **Revenue Intelligence** — Order value distribution, revenue by source

## Screenshots

<img width="2685" height="1183" alt="01_main_funnel" src="https://github.com/user-attachments/assets/cc52036e-610c-4006-91ea-c908a9f27e7b" />
<img width="2372" height="1769" alt="02_device_analysis" src="https://github.com/user-attachments/assets/fd55479c-58a4-452f-b1e8-f7acbdbdb82a" />
<img width="2383" height="1772" alt="03_traffic_source" src="https://github.com/user-attachments/assets/20db981c-9bc3-42e8-85da-d9916356725c" />
<img width="2380" height="1766" alt="04_geography" src="https://github.com/user-attachments/assets/a6311d41-4ea8-46e5-ae7e-ceaeb1eca587" />
<img width="2382" height="1771" alt="05_time_category" src="https://github.com/user-attachments/assets/87b2f751-b3b5-4d1d-b328-98bc4252395e" />
<img width="2383" height="1771" alt="06_revenue_insights" src="https://github.com/user-attachments/assets/d3570656-2103-4f79-bc2b-a30cb08d05b3" />
