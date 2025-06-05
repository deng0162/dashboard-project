import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/20240411_P27_with_region.csv")
df = df.dropna(subset=["year", "country_name_text", "total_country_article_count", "total_country_avg_sentiment"])
df["year"] = df["year"].astype(int)

target_countries = [
    "United States", "China", "United Kingdom", "France", "India",
    "Canada", "Brazil", "Greece", "South Africa", "Indonesia"
]

# Output folder
output_dir = "/home/acct/schaf/team/yiyid/projects/data_vit/Outfiles/country_combo_charts"
os.makedirs(output_dir, exist_ok=True)

# Loop over countries
for country in target_countries:
    df_country = df[df["country_name_text"] == country]

    # Keep only one row per (country, year)
    df_country_unique = df_country.drop_duplicates(subset=["country_name_text", "year"])

    if df_country_unique.empty:
        print(f"No data found for {country}.")
        continue

    # Sort by year
    df_country_unique = df_country_unique.sort_values("year")

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(df_country_unique["year"], df_country_unique["total_country_avg_sentiment"],
             color="blue", marker="o", label="Avg Sentiment")
    ax1.set_ylabel("Average Sentiment", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.bar(df_country_unique["year"], df_country_unique["total_country_article_count"],
            color="lightgray", alpha=0.7, label="Article Count")
    ax2.set_ylabel("Article Count", color="gray")
    ax2.tick_params(axis="y", labelcolor="gray")

    ax1.set_xlabel("Year")
    plt.title(f"{country} – Sentiment & Article Count Over Time")

    if len(df_country_unique["year"].unique()) > 10:
        ax1.set_xticks([y for y in df_country_unique["year"].unique() if y % 2 == 0])

    fig.tight_layout()
    output_path = os.path.join(output_dir, f"{country.replace(' ', '_')}_combo_chart.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved chart for {country} at: {output_path}")

print("All country combo charts saved.")

