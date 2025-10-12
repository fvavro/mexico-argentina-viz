import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Data/ert.csv')
mexico = df[(df['country_name'] == 'Mexico') & (df['year'] >= 1980)].copy()
argentina = df[(df['country_name'] == 'Argentina') & (df['year'] >= 1980)].copy()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Political Legacies of Neoliberal Reform: Mexico vs Argentina', 
             fontsize=14, fontweight='bold', y=0.98)

# Democratic Development in Key Periods
ax1.plot(mexico['year'], mexico['v2x_polyarchy'], 
         label='Mexico', linewidth=3, color='#1f77b4')
ax1.plot(argentina['year'], argentina['v2x_polyarchy'], 
         label='Argentina', linewidth=3, color='#ff7f0e')

ax1.axvspan(1982, 1990, alpha=0.2, color='red', label='Debt Crisis/"Lost Decade"')
ax1.axvspan(1990, 2000, alpha=0.2, color='green', label='Neoliberal Reforms (Menem/Salinas)')
ax1.axvspan(2018, 2024, alpha=0.2, color='purple', label='Contemporary Populism (AMLO/Milei)')

ax1.set_title('Democratic Development', fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Electoral Democracy Index')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Regime Stability vs Volatility
# compute year-to-year changes
mexico['dem_change'] = mexico['v2x_polyarchy'].diff()
argentina['dem_change'] = argentina['v2x_polyarchy'].diff()

ax2.bar(mexico['year'], mexico['dem_change'], alpha=0.7, label='Mexico', color='#1f77b4')
ax2.bar(argentina['year'], argentina['dem_change'], alpha=0.7, label='Argentina', color='#ff7f0e')

ax2.set_title('Democratic Stability: Year-to-Year Changes\n(Higher volatility = institutional weakness)', fontweight='bold')
ax2.set_xlabel('Year')
ax2.set_ylabel('Annual Change in Democracy Index')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Current Populist Era (2015-2024)
recent_years = range(2015, 2025)
mex_recent = mexico[mexico['year'].isin(recent_years)]
arg_recent = argentina[argentina['year'].isin(recent_years)]

ax3.plot(mex_recent['year'], mex_recent['v2x_polyarchy'], 
         label='Mexico (AMLO era)', linewidth=3, marker='o', color='#1f77b4')
ax3.plot(arg_recent['year'], arg_recent['v2x_polyarchy'], 
         label='Argentina (Milei era)', linewidth=3, marker='s', color='#ff7f0e')

# Add trend lines
z_mex = np.polyfit(mex_recent['year'], mex_recent['v2x_polyarchy'], 1)
p_mex = np.poly1d(z_mex)
z_arg = np.polyfit(arg_recent['year'], arg_recent['v2x_polyarchy'], 1)
p_arg = np.poly1d(z_arg)

ax3.plot(mex_recent['year'], p_mex(mex_recent['year']), "b--", alpha=0.7)
ax3.plot(arg_recent['year'], p_arg(arg_recent['year']), "orange", linestyle='--', alpha=0.7)

ax3.set_title('Contemporary Populist Era (2015-2024)\nDemocratic Trajectories Under AMLO and Milei', fontweight='bold')
ax3.set_xlabel('Year')
ax3.set_ylabel('Democracy Index')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Long-term Democratic Quality Comparison
periods = [
    (1980, 1989, 'Lost Decade'),
    (1990, 1999, 'Neoliberal\nReforms'), 
    (2000, 2009, 'Post-Reform'),
    (2010, 2024, 'Contemporary')
]

mexico_means = [mexico[(mexico['year'] >= start) & (mexico['year'] <= end)]['v2x_polyarchy'].mean() 
                for start, end, label in periods]
argentina_means = [argentina[(argentina['year'] >= start) & (argentina['year'] <= end)]['v2x_polyarchy'].mean() 
                   for start, end, label in periods]
labels = [label for start, end, label in periods]

x = np.arange(len(periods))
width = 0.35

ax4.bar(x - width/2, mexico_means, width, label='Mexico', color='#1f77b4', alpha=0.8)
ax4.bar(x + width/2, argentina_means, width, label='Argentina', color='#ff7f0e', alpha=0.8)

ax4.set_title('Average Democratic Quality by Period', fontweight='bold')
ax4.set_xlabel('Historical Periods')
ax4.set_ylabel('Average Democracy Index')
ax4.set_xticks(x)
ax4.set_xticklabels(labels)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ert_graph.png', dpi=300, bbox_inches='tight')
plt.show()