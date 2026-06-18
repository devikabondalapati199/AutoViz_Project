import os

os.makedirs("reports", exist_ok=True)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

def create_report(
    summary,
    correlations,
    outliers,
    insights
):

    pdf_file = "reports/analysis_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AutoViz Analysis Report",
            styles['Title']
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            str(summary),
            styles['BodyText']
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Strong Correlations",
            styles['Heading2']
        )
    )

    for item in correlations:

        content.append(
            Paragraph(
                str(item),
                styles['BodyText']
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Outlier Analysis",
            styles['Heading2']
        )
    )

    for item in outliers:

        content.append(
            Paragraph(
                str(item),
                styles['BodyText']
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Insights",
            styles['Heading2']
        )
    )

    for item in insights:

        content.append(
            Paragraph(
                item,
                styles['BodyText']
            )
        )

    doc.build(content)

    return pdf_file
