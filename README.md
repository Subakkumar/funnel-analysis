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