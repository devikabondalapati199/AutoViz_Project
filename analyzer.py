def find_strong_correlations(df):

    numeric_df = df.select_dtypes(include='number')

    corr_matrix = numeric_df.corr()

    correlations = []

    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):

            corr = corr_matrix.iloc[i, j]

            if abs(corr) >= 0.7:

                correlations.append(
                    (
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr, 2)
                    )
                )

    return correlations


def detect_outliers(df):

    outlier_columns = []

    numeric_cols = df.select_dtypes(
        include='number'
    ).columns

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outliers = (
            (df[col] < lower) |
            (df[col] > upper)
        ).sum()

        if outliers > 0:
            outlier_columns.append(
                f"{col} ({outliers} outliers)"
            )

    return outlier_columns