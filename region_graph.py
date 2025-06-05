import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/20240411_P27_with_region.csv")
df = df.dropna(subset=["year", "region", "total_country_article_count", "total_country_avg_sentiment"])
df["year"] = df["year"].astype(int)

# Output folder
output_dir = "/home/acct/schaf/team/yiyid/projects/data_vit/Outfiles/region_combo_charts"
os.makedirs(output_dir, exist_ok=True)

df_unique_country_year = df.drop_duplicates(subset=["country_name_text", "year"])

# Group by region + year then aggregate
region_yearly = df_unique_country_year.groupby(["region", "year"]).agg({
    "total_country_article_count": "sum",
    "total_country_avg_sentiment": "mean"
}).reset_index()

all_regions = region_yearly["region"].dropna().unique()

for region in all_regions:
    df_region = region_yearly[region_yearly["region"] == region].sort_values("year")

    if df_region.empty:
        print(f"No data found for region: {region}")
        continue

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(df_region["year"], df_region["total_country_avg_sentiment"],
             color="#2a9d8f", marker="o", label="Avg Sentiment")
    ax1.set_ylabel("Average Sentiment", color="#2a9d8f")
    ax1.tick_params(axis="y", labelcolor="#2a9d8f")
    ax1.grid(True)


    ax2 = ax1.twinx()
    ax2.bar(df_region["year"], df_region["total_country_article_count"],
            color="#a8dadc", alpha=0.8, label="Article Count")
    ax2.set_ylabel("Total Article Count", color="#457b9d")
    ax2.tick_params(axis="y", labelcolor="#457b9d")

    ax1.set_xlabel("Year")
    plt.title(f"{region} – Sentiment & Article Count Over Time")

    # sparse x-ticks
    if len(df_region["year"].unique()) > 10:
        ax1.set_xticks([y for y in df_region["year"].unique() if y % 2 == 0])

    fig.tight_layout()
    filename = region.replace(" ", "_").replace("/", "-")
    output_path = os.path.join(output_dir, f"{filename}_combo_chart.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved chart for region: {region} at {output_path}")

print("All region combo charts saved.")

