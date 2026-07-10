import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from ml import data

def main():
    # Load and encode data
    raw = data.load_raw()
    if len(raw) > 1000:
        raw = raw.sample(n=1000, random_state=42)
    encoded = data.encode(raw)
    
    # We only care about the features used in the model plus the target
    cols = data.FEATURE_ORDER + [data.TARGET_COL]
    df = encoded[cols]
    
    # Rename columns for better readability in the plot
    rename_map = {feat: data.FEATURE_LABELS.get(feat, feat) for feat in data.FEATURE_ORDER}
    rename_map[data.TARGET_COL] = "Diabetes (Target)"
    df = df.rename(columns=rename_map)
    
    corr = df.corr()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Custom color map
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(corr, cmap=cmap, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5},
                annot=True, fmt=".2f", annot_kws={"size": 8}, ax=ax)
                
    ax.set_title("Feature Correlation Matrix", fontweight="bold", fontsize=14, color="#4a4038", pad=20)
    plt.xticks(rotation=45, ha="right", fontsize=9, color="#4a4038")
    plt.yticks(fontsize=9, color="#4a4038")
    
    fig.tight_layout()
    # Save to presentation assets
    fig.savefig("/Users/sawe/Downloads/diabetes-presentation/assets/correlation_matrix.png", transparent=True, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
