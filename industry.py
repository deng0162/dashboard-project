import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("/home/acct/schaf/team/yiyid/projects/data_vit/Infiles/20240411_P27_with_region.csv")
df = df.dropna(subset=["sic2", "year", "total_firm_country_article_count", "total_firm_country_avg_sentiment"])
df["year"] = df["year"].astype(int)
df["sic2"] = df["sic2"].astype(int)

# Selected SIC2 industries
sic2_targets = {
    60: "Depository Institutions",
    28: "Chemicals",
    48: "Communications",
    36: "Electronics",
    37: "Transportation Equipment",
    13: "Oil & Gas Extraction"
}

output_dir = "/home/acct/schaf/team/yiyid/projects/data_vit/Outfiles/industry_combo_charts"
os.makedirs(output_dir, exist_ok=True)

for sic, industry_name in sic2_targets.items():
    df_ind = df[df["sic2"] == sic]

    if df_ind.empty:
        print(f"No data found for SIC {sic} - {industry_name}.")
        continue

    # Group by year
    yearly = df_ind.groupby("year").agg({
        "total_firm_country_article_count": "sum",
        "total_firm_country_avg_sentiment": "mean"
    }).reset_index()

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(yearly["year"], yearly["total_firm_country_avg_sentiment"],
             color="blue", marker="o", label="Avg Sentiment")
    ax1.set_ylabel("Average Sentiment", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.bar(yearly["year"], yearly["total_firm_country_article_count"],
            color="lightgray", alpha=0.7, label="Article Count")
    ax2.set_ylabel("Article Count", color="gray")
    ax2.tick_params(axis="y", labelcolor="gray")

    plt.title(f"{industry_name} (SIC {sic}) – Sentiment & Article Count Over Time")
    ax1.set_xlabel("Year")

    # X-axis 
    if len(yearly["year"]) > 10:
        x_ticks = [year for year in yearly["year"] if year % 2 == 0]
        ax1.set_xticks(x_ticks)

    fig.tight_layout()
    output_path = os.path.join(output_dir, f"{sic}_{industry_name.replace(' ', '_')}_combo_chart.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved chart for {industry_name} at: {output_path}")

print("All industry combo charts saved.")

