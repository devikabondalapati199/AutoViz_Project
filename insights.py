def generate_insights(df, correlations, outliers):

    insights = []

    insights.append(
        f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
    )

    missing = df.isnull().sum().sum()

    insights.append(
        f"Dataset contains {missing} missing values."
    )

    duplicates = df.duplicated().sum()

    insights.append(
        f"Dataset contains {duplicates} duplicate rows."
    )

    if correlations:

        strongest = max(
            correlations,
            key=lambda x: abs(x[2])
        )

        insights.append(
            f"Strongest relationship found between "
            f"{strongest[0]} and {strongest[1]} "
            f"(correlation = {strongest[2]})."
        )

    if outliers:

        insights.append(
            f"Outliers detected in {len(outliers)} column(s)."
        )

    return insights