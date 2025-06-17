# src/enhanced_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import numpy as np
import os
from preprocessing import load_and_clean_data

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Ensure output directory exists
os.makedirs('output/charts', exist_ok=True)
os.makedirs('output/interactive', exist_ok=True)

def create_enhanced_rating_distribution(df):
    """Enhanced rating distribution with multiple chart types and storytelling"""
    print("Creating enhanced rating distribution analysis...")
    
    # Create subplot figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('IMDb Top 250: Rating Distribution Deep Dive', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Enhanced histogram with KDE
    sns.histplot(data=df, x='rating', bins=15, kde=True, ax=ax1, alpha=0.7, color='#2E86AB')
    ax1.axvline(df['rating'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["rating"].mean():.2f}')
    ax1.axvline(df['rating'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median: {df["rating"].median():.2f}')
    ax1.set_title('Rating Distribution with Central Tendencies', fontsize=14, fontweight='bold')
    ax1.set_xlabel('IMDb Rating')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Box plot by decade
    sns.boxplot(data=df, x='decade', y='rating', ax=ax2, palette='viridis')
    ax2.set_title('Rating Distribution by Decade', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Decade')
    ax2.set_ylabel('IMDb Rating')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Violin plot for rating density
    sns.violinplot(data=df, y='rating', ax=ax3, color='#A23B72')
    ax3.set_title('Rating Density Distribution', fontsize=14, fontweight='bold')
    ax3.set_ylabel('IMDb Rating')
    
    # 4. Rating statistics summary
    stats_text = f"""
    Statistical Summary:
    Mean: {df['rating'].mean():.2f}
    Median: {df['rating'].median():.2f}
    Std Dev: {df['rating'].std():.2f}
    Min: {df['rating'].min():.1f}
    Max: {df['rating'].max():.1f}
    
    Key Insight:
    {np.sum(df['rating'] >= 8.5)} movies ({np.sum(df['rating'] >= 8.5)/len(df)*100:.1f}%) 
    have ratings ≥ 8.5, showing
    exceptional quality threshold
    """
    ax4.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Statistical Insights', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/charts/enhanced_rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved enhanced_rating_distribution.png")

def create_temporal_analysis(df):
    """Advanced temporal analysis with trend lines and annotations"""
    print("Creating temporal trend analysis...")
    
    # Calculate decade statistics
    decade_stats = df.groupby('decade').agg({
        'rating': ['mean', 'count', 'std'],
        'year': 'mean'
    }).round(2)
    decade_stats.columns = ['avg_rating', 'movie_count', 'rating_std', 'mid_year']
    decade_stats = decade_stats.reset_index()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle('Temporal Analysis: Evolution of Cinema Excellence', fontsize=20, fontweight='bold')
    
    # 1. Movies count by decade with trend
    bars = ax1.bar(decade_stats['decade'], decade_stats['movie_count'], 
                   color=plt.cm.viridis(np.linspace(0, 1, len(decade_stats))), alpha=0.8)
    ax1.set_title('Distribution of Top Movies Across Decades', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Decade')
    ax1.set_ylabel('Number of Movies')
    
    # Add value labels on bars
    for bar, count in zip(bars, decade_stats['movie_count']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(int(count)), ha='center', va='bottom', fontweight='bold')
    
    # 2. Average rating by decade with error bars
    ax2.errorbar(decade_stats['decade'], decade_stats['avg_rating'], 
                yerr=decade_stats['rating_std'], fmt='o-', linewidth=3, 
                markersize=8, capsize=5, color='#E74C3C')
    ax2.set_title('Average Rating Trends by Decade', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Decade')
    ax2.set_ylabel('Average IMDb Rating')
    ax2.grid(True, alpha=0.3)
    
    # Highlight best decade
    best_decade = decade_stats.loc[decade_stats['avg_rating'].idxmax(), 'decade']
    best_rating = decade_stats['avg_rating'].max()
    ax2.annotate(f'Peak Era: {best_decade}s\nRating: {best_rating:.2f}', 
                xy=(best_decade, best_rating), xytext=(best_decade+10, best_rating+0.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, fontweight='bold', color='red')
    
    # 3. Scatter plot: Year vs Rating with trend line
    ax3.scatter(df['year'], df['rating'], alpha=0.6, s=50, c=df['decade'], cmap='viridis')
    z = np.polyfit(df['year'], df['rating'], 1)
    p = np.poly1d(z)
    ax3.plot(df['year'], p(df['year']), "r--", alpha=0.8, linewidth=2, label=f'Trend: {z[0]:.4f}x + {z[1]:.2f}')
    ax3.set_title('Rating Trends Over Time', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Release Year')
    ax3.set_ylabel('IMDb Rating')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Rating volatility by decade
    ax4.bar(decade_stats['decade'], decade_stats['rating_std'], 
           color='orange', alpha=0.7)
    ax4.set_title('Rating Consistency by Decade', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Decade')
    ax4.set_ylabel('Rating Standard Deviation')
    ax4.axhline(decade_stats['rating_std'].mean(), color='red', linestyle='--', 
               label=f'Average σ: {decade_stats["rating_std"].mean():.3f}')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('output/charts/temporal_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved temporal_analysis.png")

def create_top_movies_showcase(df):
    """Enhanced top movies visualization with rich information"""
    print("Creating top movies showcase...")
    
    # Get top 10 movies
    top_movies = df.nlargest(10, 'rating').copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    fig.suptitle('Cinematic Excellence: Top-Rated Movies Analysis', fontsize=18, fontweight='bold')
    
    # 1. Top 10 horizontal bar chart
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_movies)))
    bars = ax1.barh(range(len(top_movies)), top_movies['rating'], color=colors)
    ax1.set_yticks(range(len(top_movies)))
    ax1.set_yticklabels([f"{name[:30]}..." if len(name) > 30 else name 
                        for name in top_movies['name']], fontsize=10)
    ax1.set_xlabel('IMDb Rating')
    ax1.set_title('Top 10 Highest Rated Movies', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add rating values on bars
    for i, (bar, rating) in enumerate(zip(bars, top_movies['rating'])):
        ax1.text(rating + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{rating:.1f}', va='center', fontweight='bold')
    
    # 2. Top movies by decade
    top_by_decade = df.loc[df.groupby('decade')['rating'].idxmax()]
    decades = sorted(top_by_decade['decade'].unique())
    ratings = [top_by_decade[top_by_decade['decade'] == d]['rating'].values[0] for d in decades]
    names = [top_by_decade[top_by_decade['decade'] == d]['name'].values[0] for d in decades]
    
    bars2 = ax2.bar(decades, ratings, color=plt.cm.plasma(np.linspace(0, 1, len(decades))), alpha=0.8)
    ax2.set_xlabel('Decade')
    ax2.set_ylabel('Highest Rating in Decade')
    ax2.set_title('Best Movie from Each Decade', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add movie names on bars
    for bar, name, rating in zip(bars2, names, ratings):
        short_name = name[:15] + "..." if len(name) > 15 else name
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{short_name}\n{rating:.1f}', ha='center', va='bottom', 
                fontsize=9, fontweight='bold', rotation=0)
    
    plt.tight_layout()
    plt.savefig('output/charts/top_movies_showcase.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved top_movies_showcase.png")

def create_interactive_dashboard(df):
    """Create interactive Plotly dashboard"""
    print("Creating interactive dashboard...")
    
    # 1. Interactive scatter plot: Year vs Rating
    fig1 = px.scatter(df, x='year', y='rating', 
                     hover_data=['name', 'decade'],
                     color='decade',
                     size_max=10,
                     title='Interactive Movie Timeline: Year vs Rating',
                     labels={'year': 'Release Year', 'rating': 'IMDb Rating'})
    fig1.update_layout(height=600, showlegend=True)
    fig1.write_html('output/interactive/scatter_timeline.html')
    
    # 2. Interactive histogram with decade filter
    fig2 = px.histogram(df, x='rating', color='decade', 
                       title='Rating Distribution by Decade (Interactive)',
                       labels={'rating': 'IMDb Rating', 'count': 'Number of Movies'})
    fig2.update_layout(height=500, barmode='overlay')
    fig2.update_traces(opacity=0.7)
    fig2.write_html('output/interactive/rating_histogram.html')
    
    # 3. Interactive box plot
    fig3 = px.box(df, x='decade', y='rating', 
                 hover_data=['name'],
                 title='Rating Distribution by Decade (Box Plot)')
    fig3.update_layout(height=500)
    fig3.write_html('output/interactive/decade_boxplot.html')
    
    # 4. Combined dashboard
    subplot_fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Timeline Scatter', 'Rating Distribution', 
                       'Decade Analysis', 'Top Movies'),
        specs=[[{"type": "scatter"}, {"type": "histogram"}],
               [{"type": "box"}, {"type": "bar"}]]
    )
    
    # Add scatter plot
    subplot_fig.add_trace(
        go.Scatter(x=df['year'], y=df['rating'], 
                  mode='markers', name='Movies',
                  text=df['name'], hovertemplate='%{text}<br>Year: %{x}<br>Rating: %{y}'),
        row=1, col=1
    )
    
    # Add histogram
    subplot_fig.add_trace(
        go.Histogram(x=df['rating'], name='Ratings', nbinsx=15),
        row=1, col=2
    )
    
    # Add box plot
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        subplot_fig.add_trace(
            go.Box(y=decade_data['rating'], name=f'{decade}s',
                  text=decade_data['name'], showlegend=False),
            row=2, col=1
        )
    
    # Add top movies bar
    top_5 = df.nlargest(5, 'rating')
    subplot_fig.add_trace(
        go.Bar(x=top_5['name'], y=top_5['rating'], 
               name='Top Movies', showlegend=False),
        row=2, col=2
    )
    
    subplot_fig.update_layout(height=800, title_text="IMDb Top 250 Movies - Interactive Dashboard")
    subplot_fig.write_html('output/interactive/combined_dashboard.html')
    
    print("✅ Saved interactive visualizations to output/interactive/")

def generate_insights_report(df):
    """Generate comprehensive data storytelling insights"""
    print("Generating insights report...")
    
    # Calculate key metrics
    total_movies = len(df)
    avg_rating = df['rating'].mean()
    rating_std = df['rating'].std()
    decades = df['decade'].nunique()
    
    # Decade analysis
    decade_stats = df.groupby('decade').agg({
        'rating': ['mean', 'count'],
        'year': 'mean'
    }).round(2)
    decade_stats.columns = ['avg_rating', 'count', 'mid_year']
    best_decade = decade_stats.loc[decade_stats['avg_rating'].idxmax()]
    
    # Rating distribution
    exceptional_movies = np.sum(df['rating'] >= 9.0)
    good_movies = np.sum((df['rating'] >= 8.0) & (df['rating'] < 9.0))
    
    # Create insights visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Data Story: Key Insights from IMDb Top 250', fontsize=18, fontweight='bold')
    
    # Insight 1: Quality threshold analysis
    quality_categories = ['Exceptional\n(9.0+)', 'Excellent\n(8.5-8.9)', 'Very Good\n(8.0-8.4)', 'Good\n(<8.0)']
    quality_counts = [
        np.sum(df['rating'] >= 9.0),
        np.sum((df['rating'] >= 8.5) & (df['rating'] < 9.0)),
        np.sum((df['rating'] >= 8.0) & (df['rating'] < 8.5)),
        np.sum(df['rating'] < 8.0)
    ]
    
    colors = ['#2E8B57', '#32CD32', '#FFD700', '#FFA500']
    pie = ax1.pie(quality_counts, labels=quality_categories, autopct='%1.1f%%', 
                  colors=colors, startangle=90)
    ax1.set_title('Quality Distribution Analysis', fontsize=14, fontweight='bold')
    
    # Insight 2: Temporal trends
    ax2.plot(decade_stats.index, decade_stats['avg_rating'], 'o-', linewidth=3, markersize=8)
    ax2.set_title('Average Rating Evolution by Decade', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Decade')
    ax2.set_ylabel('Average Rating')
    ax2.grid(True, alpha=0.3)
    
    # Highlight golden age
    golden_decade = decade_stats['avg_rating'].idxmax()
    golden_rating = decade_stats['avg_rating'].max()
    ax2.annotate(f'Golden Age: {golden_decade}s', 
                xy=(golden_decade, golden_rating), 
                xytext=(golden_decade-5, golden_rating+0.05),
                arrowprops=dict(arrowstyle='->', color='gold', lw=2),
                fontsize=12, fontweight='bold', color='gold')
    
    # Insight 3: Rating consistency
    ax3.bar(decade_stats.index, decade_stats['count'], alpha=0.7, color='skyblue')
    ax3.set_title('Movie Count by Decade', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Decade')
    ax3.set_ylabel('Number of Movies')
    
    # Insight 4: Key statistics summary
    insights_text = f"""
    📊 DATASET OVERVIEW
    • Total Movies: {total_movies}
    • Rating Range: {df['rating'].min():.1f} - {df['rating'].max():.1f}
    • Average Rating: {avg_rating:.2f} ± {rating_std:.2f}
    
    🏆 QUALITY INSIGHTS
    • {exceptional_movies} movies ({exceptional_movies/total_movies*100:.1f}%) rated 9.0+
    • {good_movies} movies ({good_movies/total_movies*100:.1f}%) rated 8.0-8.9
    
    📈 TEMPORAL INSIGHTS
    • Golden Age: {golden_decade}s (avg: {golden_rating:.2f})
    • Span: {decades} decades represented
    • Most Productive: {decade_stats.loc[decade_stats['count'].idxmax()].name}s ({decade_stats['count'].max()} movies)
    
    🎯 KEY FINDINGS
    • Consistent high quality across eras
    • {golden_decade}s showed peak cinematic excellence
    • Modern classics maintain historical standards
    """
    
    ax4.text(0.05, 0.95, insights_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Executive Summary', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/charts/insights_report.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved insights_report.png")

def main():
    """Main function to generate all enhanced visualizations"""
    try:
        print("🎬 Starting Enhanced Movie Analysis Visualization...")
        df = load_and_clean_data()
        
        if df.empty:
            print("❌ Error: DataFrame is empty")
            return
        
        print(f"📊 Loaded {len(df)} movies for analysis")
        
        # Generate all visualizations
        create_enhanced_rating_distribution(df)
        create_temporal_analysis(df)
        create_top_movies_showcase(df)
        create_interactive_dashboard(df)
        generate_insights_report(df)
        
        print("\n🎉 All visualizations generated successfully!")
        print("📁 Check the following directories:")
        print("   • output/charts/ - Static visualizations")
        print("   • output/interactive/ - Interactive HTML dashboards")
        
    except Exception as e:
        print(f"❌ Error in enhanced visualization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()