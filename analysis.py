import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
import os
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor':   '#161b27',
    'axes.edgecolor':   '#30363d',
    'axes.labelcolor':  '#e6edf3',
    'text.color':       '#e6edf3',
    'xtick.color':      '#8b949e',
    'ytick.color':      '#8b949e',
    'grid.color':       '#21262d',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
    'figure.dpi':       120
})

COLORS  = ['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657',
           '#79c0ff','#56d364','#ff7b72','#bc8cff','#ffc680']
FUNNEL_STEPS = ['landing_page','product_view','add_to_cart','checkout','purchase']
STEP_LABELS  = ['Landing Page','Product View','Add to Cart','Checkout','Purchase']

os.makedirs('outputs', exist_ok=True)

def save(name):
    plt.tight_layout()
    plt.savefig(f'outputs/{name}.png', dpi=150,
                bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"Saved: {name}.png")

def load_data():
    if not os.path.exists('data/funnel_data.csv'):
        print("Generating data first...")
        from data_generator import generate_users
        generate_users(50000)
    df = pd.read_csv('data/funnel_data.csv', parse_dates=['date'])
    return df

def get_funnel_counts(df):
    counts = []
    for step in FUNNEL_STEPS:
        mask = df['reached_step'].isin(
            FUNNEL_STEPS[FUNNEL_STEPS.index(step):]
        ) | (df['reached_step'] == step)
        n = (df['reached_step'].apply(
            lambda x: FUNNEL_STEPS.index(x) >= FUNNEL_STEPS.index(step)
            if x in FUNNEL_STEPS else False
        )).sum()
        counts.append(n)
    return counts

# ─────────────────────────────────────────
def plot1_main_funnel(df):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('E-Commerce Conversion Funnel — Overview',
                 fontsize=20, fontweight='bold', color='#e6edf3')

    counts = get_funnel_counts(df)
    total  = counts[0]

    # Funnel bars
    ax = axes[0]
    bar_colors = ['#58a6ff','#3fb950','#ffa657','#f78166','#d2a8ff']
    bars = ax.barh(STEP_LABELS[::-1], counts[::-1],
                   color=bar_colors[::-1], alpha=0.88, height=0.55)
    ax.set_title('Users at Each Funnel Stage',
                 fontweight='bold', color='#e6edf3', fontsize=13)
    ax.set_xlabel('Number of Users')
    ax.grid(axis='x', alpha=0.3)
    for bar, val, label in zip(bars, counts[::-1], STEP_LABELS[::-1]):
        pct = val / total * 100
        ax.text(val + 200, bar.get_y() + bar.get_height()/2,
                f'{val:,}  ({pct:.1f}%)',
                va='center', fontsize=10, color='#e6edf3', fontweight='bold')

    # Drop-off waterfall
    ax = axes[1]
    drop_pcts = []
    for i in range(1, len(counts)):
        drop = (counts[i-1] - counts[i]) / counts[i-1] * 100
        drop_pcts.append(drop)

    drop_labels = [f'{STEP_LABELS[i]}→{STEP_LABELS[i+1]}'
                   for i in range(len(STEP_LABELS)-1)]
    drop_colors = ['#ef4444' if d > 40 else '#f97316' if d > 25 else '#fbbf24'
                   for d in drop_pcts]
    bars2 = ax.bar(range(len(drop_pcts)), drop_pcts,
                   color=drop_colors, alpha=0.88, width=0.55)
    ax.set_title('Drop-off Rate Between Each Stage',
                 fontweight='bold', color='#e6edf3', fontsize=13)
    ax.set_ylabel('Drop-off Rate (%)')
    ax.set_xticks(range(len(drop_labels)))
    ax.set_xticklabels(drop_labels, rotation=20, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars2, drop_pcts):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', fontsize=11,
                color='#e6edf3', fontweight='bold')

    legend_patches = [
        mpatches.Patch(color='#ef4444', label='Critical (>40%)'),
        mpatches.Patch(color='#f97316', label='High (25-40%)'),
        mpatches.Patch(color='#fbbf24', label='Moderate (<25%)')
    ]
    ax.legend(handles=legend_patches, fontsize=9, loc='upper right')

    save('01_main_funnel')

# ─────────────────────────────────────────
def plot2_device_analysis(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Device Analysis — How Platform Affects Conversion',
                 fontsize=18, fontweight='bold', color='#e6edf3')

    devices = df['device'].unique()
    dev_colors = {'mobile': COLORS[0], 'desktop': COLORS[1], 'tablet': COLORS[2]}

    # Conversion rate by device
    ax = axes[0, 0]
    dev_conv = df.groupby('device')['converted'].mean() * 100
    bars = ax.bar(dev_conv.index, dev_conv.values,
                  color=[dev_colors[d] for d in dev_conv.index], alpha=0.88)
    ax.set_title('Conversion Rate by Device', fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Conversion Rate (%)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, dev_conv.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.1,
                f'{val:.1f}%', ha='center', fontsize=11,
                color='#e6edf3', fontweight='bold')

    # Funnel by device
    ax = axes[0, 1]
    for i, device in enumerate(devices):
        sub = df[df['device'] == device]
        counts = get_funnel_counts(sub)
        pcts = [c / counts[0] * 100 for c in counts]
        ax.plot(STEP_LABELS, pcts, marker='o', linewidth=2.5,
                markersize=7, label=device.capitalize(),
                color=dev_colors[device])
    ax.set_title('Funnel Progression by Device', fontweight='bold', color='#e6edf3')
    ax.set_ylabel('% of Users Remaining')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.tick_params(axis='x', rotation=15)

    # User share by device
    ax = axes[1, 0]
    dev_counts = df['device'].value_counts()
    ax.pie(dev_counts.values, labels=[d.capitalize() for d in dev_counts.index],
           autopct='%1.1f%%', colors=[dev_colors[d] for d in dev_counts.index],
           startangle=90, textprops={'color': '#e6edf3', 'fontsize': 10})
    ax.set_title('User Share by Device', fontweight='bold', color='#e6edf3')

    # Avg order value by device
    ax = axes[1, 1]
    dev_aov = df[df['converted'] == 1].groupby('device')['order_value'].mean()
    bars = ax.bar(dev_aov.index, dev_aov.values,
                  color=[dev_colors[d] for d in dev_aov.index], alpha=0.88)
    ax.set_title('Avg Order Value by Device', fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Avg Order Value (USD)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, dev_aov.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1,
                f'${val:.2f}', ha='center', fontsize=11,
                color='#e6edf3', fontweight='bold')

    save('02_device_analysis')

# ─────────────────────────────────────────
def plot3_traffic_source(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Traffic Source Analysis — Where Do Your Best Users Come From?',
                 fontsize=18, fontweight='bold', color='#e6edf3')

    sources = df['traffic_source'].value_counts().index.tolist()

    # Conversion rate by source
    ax = axes[0, 0]
    src_conv = (df.groupby('traffic_source')['converted']
            .mean() * 100)
    src_conv = src_conv.sort_values(ascending=False)
    src_conv = df.groupby('traffic_source')['converted'].mean() * 100
    src_conv = src_conv.sort_values(ascending=False)
    src_colors = [COLORS[i] for i in range(len(src_conv))]
    bars = ax.bar(range(len(src_conv)), src_conv.values,
                  color=src_colors, alpha=0.88)
    ax.set_xticks(range(len(src_conv)))
    ax.set_xticklabels([s.replace('_', '\n') for s in src_conv.index],
                       fontsize=9)
    ax.set_title('Conversion Rate by Traffic Source',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Conversion Rate (%)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, src_conv.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.05,
                f'{val:.1f}%', ha='center', fontsize=10,
                color='#e6edf3', fontweight='bold')

    # Users by source
    ax = axes[0, 1]
    src_users = df['traffic_source'].value_counts()
    ax.pie(src_users.values,
           labels=[s.replace('_', ' ').title() for s in src_users.index],
           autopct='%1.1f%%', colors=COLORS[:len(src_users)],
           startangle=90, textprops={'color': '#e6edf3', 'fontsize': 9})
    ax.set_title('User Distribution by Source',
                 fontweight='bold', color='#e6edf3')

    # Revenue by source
    ax = axes[1, 0]
    src_rev = (df[df['converted'] == 1]
               .groupby('traffic_source')['order_value']
               .sum()
               .sort_values(ascending=False))
    bars = ax.bar(range(len(src_rev)), src_rev.values,
                  color=COLORS[:len(src_rev)], alpha=0.88)
    ax.set_xticks(range(len(src_rev)))
    ax.set_xticklabels([s.replace('_', '\n') for s in src_rev.index], fontsize=9)
    ax.set_title('Total Revenue by Traffic Source',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Total Revenue (USD)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, src_rev.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 500,
                f'${val/1000:.0f}K', ha='center', fontsize=10,
                color='#e6edf3', fontweight='bold')

    # Funnel by source (checkout to purchase conversion)
    ax = axes[1, 1]
    src_step_conv = []
    for src in src_conv.index:
        sub = df[df['traffic_source'] == src]
        counts = get_funnel_counts(sub)
        src_step_conv.append({
            'source': src.replace('_', ' ').title(),
            'landing_to_purchase': counts[-1] / counts[0] * 100,
            'checkout_to_purchase': counts[-1] / counts[-2] * 100 if counts[-2] > 0 else 0
        })
    src_df = pd.DataFrame(src_step_conv).set_index('source')
    x = np.arange(len(src_df))
    w = 0.35
    ax.bar(x - w/2, src_df['landing_to_purchase'], w,
           label='Overall Conversion', color=COLORS[0], alpha=0.88)
    ax.bar(x + w/2, src_df['checkout_to_purchase'], w,
           label='Checkout→Purchase', color=COLORS[1], alpha=0.88)
    ax.set_xticks(x)
    ax.set_xticklabels(src_df.index, rotation=15, ha='right', fontsize=8)
    ax.set_title('Conversion Rates by Source',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Conversion Rate (%)')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    save('03_traffic_source')

# ─────────────────────────────────────────
def plot4_geography(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Geographic Analysis — Where Are Your Customers?',
                 fontsize=18, fontweight='bold', color='#e6edf3')

    # Conversion by country
    ax = axes[0, 0]
    ctry_conv = df.groupby('country')['converted'].mean() * 100
    ctry_conv = ctry_conv.sort_values(ascending=False)
    ctry_conv = df.groupby('country')['converted'].mean() * 100
    ctry_conv = ctry_conv.sort_values(ascending=False)
    colors_ctry = ['#3fb950' if v >= 7 else '#ffa657' if v >= 5 else '#f78166'
                   for v in ctry_conv.values]
    bars = ax.barh(ctry_conv.index[::-1], ctry_conv.values[::-1],
                   color=list(reversed(colors_ctry)), alpha=0.88)
    ax.set_title('Conversion Rate by Country',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Conversion Rate (%)')
    ax.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, ctry_conv.values[::-1]):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=10,
                color='#e6edf3', fontweight='bold')

    # Revenue by country
    ax = axes[0, 1]
    ctry_rev = (df[df['converted'] == 1]
                .groupby('country')['order_value']
                .sum()
                .sort_values(ascending=False))
    bars = ax.bar(range(len(ctry_rev)), ctry_rev.values,
                  color=COLORS[:len(ctry_rev)], alpha=0.88)
    ax.set_xticks(range(len(ctry_rev)))
    ax.set_xticklabels(ctry_rev.index, rotation=20, ha='right', fontsize=9)
    ax.set_title('Total Revenue by Country',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Revenue (USD)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, ctry_rev.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 300,
                f'${val/1000:.0f}K', ha='center', fontsize=9,
                color='#e6edf3', fontweight='bold')

    # Users by country
    ax = axes[1, 0]
    ctry_users = df['country'].value_counts()
    ax.pie(ctry_users.values,
           labels=ctry_users.index,
           autopct='%1.1f%%', colors=COLORS[:len(ctry_users)],
           startangle=90, textprops={'color': '#e6edf3', 'fontsize': 9})
    ax.set_title('User Distribution by Country',
                 fontweight='bold', color='#e6edf3')

    # Avg order value by country
    ax = axes[1, 1]
    ctry_aov = (df[df['converted'] == 1]
                .groupby('country')['order_value']
                .mean()
                .sort_values(ascending=False))
    bars = ax.barh(ctry_aov.index[::-1], ctry_aov.values[::-1],
                   color=COLORS[3], alpha=0.88)
    ax.set_title('Avg Order Value by Country',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Avg Order Value (USD)')
    ax.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, ctry_aov.values[::-1]):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'${val:.2f}', va='center', fontsize=10,
                color='#e6edf3', fontweight='bold')

    save('04_geography')

# ─────────────────────────────────────────
def plot5_time_category(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Time & Category Insights — When and What Converts Best?',
                 fontsize=18, fontweight='bold', color='#e6edf3')

    # Monthly conversion trend
    ax = axes[0, 0]
    monthly = df.groupby('month').agg(
        users=('user_id', 'count'),
        conversions=('converted', 'sum')
    )
    monthly['rate'] = monthly['conversions'] / monthly['users'] * 100
    month_names = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']
    ax.fill_between(monthly.index, monthly['rate'],
                    alpha=0.3, color=COLORS[0])
    ax.plot(monthly.index, monthly['rate'],
            color=COLORS[0], linewidth=2.5, marker='o', markersize=6)
    ax.set_title('Monthly Conversion Rate Trend',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Month')
    ax.set_ylabel('Conversion Rate (%)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names, fontsize=8)
    ax.grid(alpha=0.3)

    # Hourly conversion pattern
    ax = axes[0, 1]
    hourly = df.groupby('hour')['converted'].mean() * 100
    peak_hour = hourly.idxmax()
    colors_h = [COLORS[2] if h == peak_hour else COLORS[0] for h in hourly.index]
    ax.bar(hourly.index, hourly.values, color=colors_h, alpha=0.88, width=0.8)
    ax.set_title('Conversion Rate by Hour of Day',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Hour (24h)')
    ax.set_ylabel('Conversion Rate (%)')
    ax.grid(axis='y', alpha=0.3)
    ax.annotate(f'Peak: {peak_hour}:00',
                xy=(peak_hour, hourly[peak_hour]),
                xytext=(peak_hour + 2, hourly[peak_hour] + 0.3),
                arrowprops=dict(arrowstyle='->', color=COLORS[2]),
                color=COLORS[2], fontsize=9, fontweight='bold')

    # Category conversion rate
    ax = axes[1, 0]
    cat_conv = df.groupby('category')['converted'].mean() * 100
    cat_conv = cat_conv.sort_values(ascending=False)
    colors_cat = ['#3fb950' if v >= 7 else '#ffa657' if v >= 5 else '#f78166'
                  for v in cat_conv.values]
    bars = ax.bar(range(len(cat_conv)), cat_conv.values,
                  color=colors_cat, alpha=0.88)
    ax.set_xticks(range(len(cat_conv)))
    ax.set_xticklabels(cat_conv.index, rotation=20, ha='right', fontsize=9)
    ax.set_title('Conversion Rate by Category',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Conversion Rate (%)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, cat_conv.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.05,
                f'{val:.1f}%', ha='center', fontsize=9,
                color='#e6edf3', fontweight='bold')

    # Day of week pattern
    ax = axes[1, 1]
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_conv = df.groupby('day_of_week')['converted'].mean() * 100
    day_conv = day_conv.reindex(day_order)
    colors_day = [COLORS[1] if d in ['Saturday','Sunday'] else COLORS[0]
                  for d in day_order]
    bars = ax.bar(range(7), day_conv.values, color=colors_day, alpha=0.88)
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], fontsize=10)
    ax.set_title('Conversion Rate by Day of Week',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Conversion Rate (%)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, day_conv.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.05,
                f'{val:.1f}%', ha='center', fontsize=9,
                color='#e6edf3', fontweight='bold')
    legend_patches = [
        mpatches.Patch(color=COLORS[1], label='Weekend'),
        mpatches.Patch(color=COLORS[0], label='Weekday')
    ]
    ax.legend(handles=legend_patches, fontsize=9)

    save('05_time_category')

# ─────────────────────────────────────────
def plot6_revenue_insights(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Revenue Intelligence — Where Does the Money Come From?',
                 fontsize=18, fontweight='bold', color='#e6edf3')

    converted = df[df['converted'] == 1].copy()

    # Order value distribution
    ax = axes[0, 0]
    ax.hist(converted['order_value'], bins=60,
            color=COLORS[1], alpha=0.85, edgecolor='none')
    ax.axvline(converted['order_value'].median(),
               color=COLORS[2], linestyle='--',
               label=f"Median: ${converted['order_value'].median():.2f}")
    ax.axvline(converted['order_value'].mean(),
               color=COLORS[4], linestyle='--',
               label=f"Mean: ${converted['order_value'].mean():.2f}")
    ax.set_title('Order Value Distribution',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Order Value (USD)')
    ax.set_ylabel('Number of Orders')
    ax.legend()
    ax.grid(alpha=0.3)

    # Revenue by category
    ax = axes[0, 1]
    cat_rev = (converted.groupby('category')['order_value']
               .sum()
               .sort_values(ascending=False))
    bars = ax.bar(range(len(cat_rev)), cat_rev.values,
                  color=COLORS[:len(cat_rev)], alpha=0.88)
    ax.set_xticks(range(len(cat_rev)))
    ax.set_xticklabels(cat_rev.index, rotation=20, ha='right', fontsize=9)
    ax.set_title('Total Revenue by Category',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Revenue (USD)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, cat_rev.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 200,
                f'${val/1000:.0f}K', ha='center',
                fontsize=9, color='#e6edf3', fontweight='bold')

    # Monthly revenue trend
    ax = axes[1, 0]
    monthly_rev = converted.groupby('month')['order_value'].sum()
    month_names = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']
    ax.fill_between(monthly_rev.index, monthly_rev.values,
                    alpha=0.3, color=COLORS[4])
    ax.plot(monthly_rev.index, monthly_rev.values,
            color=COLORS[4], linewidth=2.5, marker='o', markersize=6)
    ax.set_title('Monthly Revenue Trend',
                 fontweight='bold', color='#e6edf3')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (USD)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names, fontsize=8)
    ax.grid(alpha=0.3)

    # Revenue per user by traffic source
    ax = axes[1, 1]
    src_rpu = {}
    for src in df['traffic_source'].unique():
        sub = df[df['traffic_source'] == src]
        total_rev = sub[sub['converted'] == 1]['order_value'].sum()
        total_users = len(sub)
        src_rpu[src.replace('_', ' ').title()] = total_rev / total_users
    rpu_series = pd.Series(src_rpu).sort_values(ascending=False)
    bars = ax.bar(range(len(rpu_series)), rpu_series.values,
                  color=COLORS[:len(rpu_series)], alpha=0.88)
    ax.set_xticks(range(len(rpu_series)))
    ax.set_xticklabels(rpu_series.index, rotation=15,
                       ha='right', fontsize=9)
    ax.set_title('Revenue Per User by Traffic Source',
                 fontweight='bold', color='#e6edf3')
    ax.set_ylabel('Revenue Per User (USD)')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, rpu_series.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.1,
                f'${val:.2f}', ha='center', fontsize=10,
                color='#e6edf3', fontweight='bold')

    save('06_revenue_insights')

# ─────────────────────────────────────────
def print_key_findings(df):
    converted = df[df['converted'] == 1]
    counts = get_funnel_counts(df)

    print("\n" + "="*60)
    print("KEY FINDINGS — FUNNEL ANALYSIS")
    print("="*60)

    print(f"\n📊 Overview:")
    print(f"   Total users:     {len(df):,}")
    print(f"   Total converted: {len(converted):,}")
    print(f"   Overall CVR:     {len(converted)/len(df)*100:.2f}%")
    print(f"   Total revenue:   ${converted['order_value'].sum():,.2f}")
    print(f"   Avg order value: ${converted['order_value'].mean():.2f}")

    print(f"\n🔻 Funnel Drop-offs:")
    for i in range(len(counts)-1):
        drop = (counts[i] - counts[i+1]) / counts[i] * 100
        print(f"   {STEP_LABELS[i]} → {STEP_LABELS[i+1]}: "
              f"{drop:.1f}% drop ({counts[i]:,} → {counts[i+1]:,})")

    print(f"\n📱 Best Device:")
    dev = df.groupby('device')['converted'].mean() * 100
    print(f"   {dev.idxmax().capitalize()} — {dev.max():.1f}% CVR")

    print(f"\n🌍 Best Country:")
    ctry = df.groupby('country')['converted'].mean() * 100
    print(f"   {ctry.idxmax()} — {ctry.max():.1f}% CVR")

    print(f"\n📣 Best Traffic Source:")
    src = df.groupby('traffic_source')['converted'].mean() * 100
    print(f"   {src.idxmax().replace('_',' ').title()} — {src.max():.1f}% CVR")

    print(f"\n🛍️ Best Category:")
    cat = df.groupby('category')['converted'].mean() * 100
    print(f"   {cat.idxmax()} — {cat.max():.1f}% CVR")

    print("\n" + "="*60)

# ─────────────────────────────────────────
if __name__ == '__main__':
    df = load_data()
    print_key_findings(df)
    print("\nGenerating visualizations...")
    plot1_main_funnel(df)
    plot2_device_analysis(df)
    plot3_traffic_source(df)
    plot4_geography(df)
    plot5_time_category(df)
    plot6_revenue_insights(df)
    print("\n✅ All done! Check the outputs/ folder.")