import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def make_chart():
    models = ["Logistic\nRegression", "Random\nForest", "Gradient\nBoosting", "Hybrid\nEnsemble"]
    # CV AUC values from the output
    auc = [0.728, 0.702, 0.738, 0.739]

    # Colors
    GREEN = "#4aa87a"
    CORAL = "#e8896a"
    TEAL = "#7bb0c4"
    INK = "#4a4038"

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "text.color": INK, "axes.labelcolor": INK,
        "axes.titlecolor": INK, "axes.titleweight": "bold", "xtick.color": INK,
        "ytick.color": INK, "axes.edgecolor": "#d9cfc4", "grid.color": "#ece4d9",
        "figure.dpi": 130,
    })

    fig, ax = plt.subplots(figsize=(8.5, 6))
    colors = [TEAL, TEAL, TEAL, CORAL]
    bars = ax.bar(models, auc, color=colors, width=0.6)
    
    ax.set_ylim(0.65, 0.8)
    ax.set_ylabel("Cross-Validated ROC-AUC")
    ax.set_title("Model Comparison: CV AUC Scores")

    # Add text labels on bars
    for bar, val in zip(bars, auc):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.002, f"{val:.3f}", ha='center', va='bottom', fontweight='bold', color=INK)

    fig.tight_layout()
    fig.savefig("/Users/sawe/Downloads/diabetes-presentation/assets/model_comparison.png", transparent=True, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    make_chart()
