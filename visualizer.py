import os
import matplotlib.pyplot as plt
import seaborn as sns


def create_histograms(df):

    os.makedirs(
        "generated_charts",
        exist_ok=True
    )

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_cols:

        plt.figure(figsize=(6, 4))

        sns.histplot(
            df[col],
            kde=True
        )

        plt.title(
            f"Distribution of {col}"
        )

        plt.savefig(
            f"generated_charts/{col}_hist.png"
        )

        plt.close()


def create_boxplots(df):

    os.makedirs(
        "generated_charts",
        exist_ok=True
    )

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_cols:

        plt.figure(figsize=(8, 4))

        sns.boxplot(
            x=df[col]
        )

        plt.title(
            f"Boxplot - {col}"
        )

        plt.savefig(
            f"generated_charts/{col}_box.png"
        )

        plt.close()


def create_scatter_plot(
    df,
    x_col,
    y_col
):

    os.makedirs(
        "generated_charts",
        exist_ok=True
    )

    plt.figure(figsize=(8, 6))

    sns.scatterplot(
        data=df,
        x=x_col,
        y=y_col
    )

    plt.title(
        f"{x_col} vs {y_col}"
    )

    plt.savefig(
        "generated_charts/scatter.png"
    )

    plt.close()