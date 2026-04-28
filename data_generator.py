import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

FUNNEL_STEPS = [
    'landing_page',
    'product_view',
    'add_to_cart',
    'checkout',
    'purchase'
]

DROP_RATES = {
    'landing_page':  0.00,
    'product_view':  0.38,
    'add_to_cart':   0.52,
    'checkout':      0.35,
    'purchase':      0.25
}

DEVICES = {
    'mobile':  0.55,
    'desktop': 0.35,
    'tablet':  0.10
}

DEVICE_DROP_MULTIPLIER = {
    'mobile':  1.25,
    'desktop': 0.80,
    'tablet':  1.10
}

TRAFFIC_SOURCES = {
    'organic_search': 0.30,
    'paid_ads':       0.25,
    'social_media':   0.20,
    'email':          0.15,
    'direct':         0.10
}

SOURCE_DROP_MULTIPLIER = {
    'organic_search': 0.90,
    'paid_ads':       1.10,
    'social_media':   1.20,
    'email':          0.75,
    'direct':         0.85
}

COUNTRIES = {
    'India':          0.30,
    'United States':  0.25,
    'United Kingdom': 0.12,
    'Germany':        0.10,
    'Brazil':         0.08,
    'Canada':         0.07,
    'Australia':      0.08
}

COUNTRY_DROP_MULTIPLIER = {
    'India':          1.15,
    'United States':  0.85,
    'United Kingdom': 0.90,
    'Germany':        0.88,
    'Brazil':         1.20,
    'Canada':         0.87,
    'Australia':      0.92
}

CATEGORIES = ['Electronics', 'Fashion', 'Books', 'Home & Kitchen',
              'Sports', 'Beauty', 'Toys', 'Automotive']

CATEGORY_DROP_MULTIPLIER = {
    'Electronics':    1.20,
    'Fashion':        0.90,
    'Books':          0.75,
    'Home & Kitchen': 1.00,
    'Sports':         0.95,
    'Beauty':         0.85,
    'Toys':           1.05,
    'Automotive':     1.30
}

def generate_users(n=50000):
    print(f"Generating {n:,} user sessions...")

    devices = np.random.choice(
        list(DEVICES.keys()),
        size=n,
        p=list(DEVICES.values())
    )
    sources = np.random.choice(
        list(TRAFFIC_SOURCES.keys()),
        size=n,
        p=list(TRAFFIC_SOURCES.values())
    )
    countries = np.random.choice(
        list(COUNTRIES.keys()),
        size=n,
        p=list(COUNTRIES.values())
    )
    categories = np.random.choice(CATEGORIES, size=n)

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta = (end_date - start_date).days
    dates = [start_date + timedelta(days=random.randint(0, delta),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59))
             for _ in range(n)]

    ages = np.random.randint(18, 65, size=n)
    session_durations = np.random.exponential(scale=180, size=n).astype(int)
    session_durations = np.clip(session_durations, 10, 1800)

    records = []
    user_ids = [f"U{str(i).zfill(6)}" for i in range(1, n+1)]

    for i in range(n):
        device = devices[i]
        source = sources[i]
        country = countries[i]
        category = categories[i]
        date = dates[i]

        reached_step = 'landing_page'
        dropped_at = None

        for step in FUNNEL_STEPS[1:]:
            base_drop = DROP_RATES[step]
            adjusted_drop = (base_drop
                             * DEVICE_DROP_MULTIPLIER[device]
                             * SOURCE_DROP_MULTIPLIER[source]
                             * COUNTRY_DROP_MULTIPLIER[country]
                             * CATEGORY_DROP_MULTIPLIER[category])
            adjusted_drop = min(adjusted_drop, 0.95)

            if np.random.random() < adjusted_drop:
                dropped_at = step
                break
            else:
                reached_step = step

        order_value = None
        if reached_step == 'purchase':
            base_values = {
                'Electronics': (150, 800),
                'Fashion': (30, 200),
                'Books': (10, 60),
                'Home & Kitchen': (40, 300),
                'Sports': (25, 250),
                'Beauty': (15, 150),
                'Toys': (20, 120),
                'Automotive': (50, 500)
            }
            low, high = base_values[category]
            order_value = round(np.random.uniform(low, high), 2)

        records.append({
            'user_id': user_ids[i],
            'date': date,
            'month': date.month,
            'day_of_week': date.strftime('%A'),
            'hour': date.hour,
            'device': device,
            'traffic_source': source,
            'country': country,
            'category': category,
            'age': ages[i],
            'session_duration_sec': session_durations[i],
            'reached_step': reached_step,
            'dropped_at': dropped_at if dropped_at else 'none',
            'converted': 1 if reached_step == 'purchase' else 0,
            'order_value': order_value
        })

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    os.makedirs('data', exist_ok=True)
    df.to_csv('data/funnel_data.csv', index=False)
    print(f"Saved: data/funnel_data.csv")
    print(f"Total users: {len(df):,}")
    print(f"Conversions: {df['converted'].sum():,} ({df['converted'].mean()*100:.1f}%)")
    return df

if __name__ == '__main__':
    df = generate_users(50000)
    print(df.head())