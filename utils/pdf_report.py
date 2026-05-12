from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def create_pdf(
    pregnancies,
    glucose,
    blood_pressure,
    bmi,
    age,
    risk,
    bmi_status
):

    pdf_file = "diabetes_report.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    elements = []

    # =====================================================
    # TITLE
    # =====================================================

    title = Paragraph(
        "<font size=22 color='#0077ff'><b>AI Diabetes Prediction Report</b></font>",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # =====================================================
    # SUBTITLE
    # =====================================================

    subtitle = Paragraph(
        "<font size=12 color='grey'>Professional Healthcare Analytics Summary</font>",
        styles['BodyText']
    )

    elements.append(subtitle)

    elements.append(Spacer(1, 20))

    # =====================================================
    # PATIENT DATA TABLE
    # =====================================================

    patient_data = [

        ["Parameter", "Value"],

        ["Pregnancies", pregnancies],

        ["Glucose", glucose],

        ["Blood Pressure", blood_pressure],

        ["BMI", bmi],

        ["Age", age],

        ["Diabetes Risk", f"{risk:.2f}%"],

        ["BMI Status", bmi_status]
    ]

    table = Table(
        patient_data,
        colWidths=[220, 220]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0077ff')),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#eaf4ff')),

        ('GRID', (0, 0), (-1, -1), 1, colors.grey),

        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),

        ('FONTSIZE', (0, 1), (-1, -1), 12),

        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),

        ('TOPPADDING', (0, 1), (-1, -1), 10),

    ]))

    elements.append(table)

    elements.append(Spacer(1, 30))

    # =====================================================
    # HEALTH ANALYSIS
    # =====================================================

    analysis_title = Paragraph(
        "<font size=18 color='#0077ff'><b>Health Analysis</b></font>",
        styles['Heading2']
    )

    elements.append(analysis_title)

    elements.append(Spacer(1, 10))

    # =====================================================
    # INSIGHTS
    # =====================================================

    insights = []

    # GLUCOSE
    if glucose > 140:

        insights.append(
            "• High glucose detected. Reduce sugar intake and monitor glucose regularly."
        )

    else:

        insights.append(
            "• Glucose level appears within healthy range."
        )

    # BLOOD PRESSURE
    if blood_pressure > 90:

        insights.append(
            "• Blood pressure is higher than normal. Reduce salt intake and stress."
        )

    else:

        insights.append(
            "• Blood pressure looks stable."
        )

    # BMI
    if bmi >= 30:

        insights.append(
            "• BMI indicates obesity. Regular exercise and healthy diet recommended."
        )

    elif bmi >= 25:

        insights.append(
            "• BMI indicates overweight condition. Maintain healthy activity."
        )

    else:

        insights.append(
            "• BMI looks healthy."
        )

    # RISK
    if risk >= 70:

        insights.append(
            "• Immediate medical consultation is recommended."
        )

    elif risk >= 50:

        insights.append(
            "• Moderate diabetes risk detected. Lifestyle improvements recommended."
        )

    else:

        insights.append(
            "• Overall health indicators appear stable."
        )

    # ADD INSIGHTS
    for point in insights:

        para = Paragraph(
            f"<font size=12>{point}</font>",
            styles['BodyText']
        )

        elements.append(para)

        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 20))

    # =====================================================
    # HEALTH SCORE
    # =====================================================

    health_score = 100 - risk

    if health_score < 0:
        health_score = 0

    score_title = Paragraph(
        f"<font size=18 color='#0077ff'><b>AI Health Score: {health_score:.0f}/100</b></font>",
        styles['Heading2']
    )

    elements.append(score_title)

    elements.append(Spacer(1, 10))

    # STATUS
    if health_score >= 80:

        status = "Excellent Health"

    elif health_score >= 60:

        status = "Moderate Health"

    elif health_score >= 40:

        status = "Health Needs Attention"

    else:

        status = "Critical Health Risk"

    status_para = Paragraph(
        f"<font size=14 color='green'><b>Status:</b> {status}</font>",
        styles['BodyText']
    )

    elements.append(status_para)

    elements.append(Spacer(1, 25))

    # =====================================================
    # FOOTER
    # =====================================================

    footer = Paragraph(
        "<font size=10 color='grey'>Generated by AI Diabetes Prediction System</font>",
        styles['BodyText']
    )

    elements.append(footer)

    # BUILD PDF
    doc.build(elements)

    return pdf_file