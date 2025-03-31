from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def recommend_strategy(company_profit):
    if company_profit <= 300_000:
        strategy = "ב' – משיכת שכר גבוה (מלא או כמעט מלא)"
        explanation = "משיכת כל הרווח כשכר כדי לנצל את מדרגות המס הנמוכות ולהימנע ממס חברות ודיבידנד."
        tax_paid = 95000
        net_to_owner = 205000
    elif 300_001 <= company_profit <= 500_000:
        strategy = "ב' או ג' – שילוב מתחיל להיות משתלם"
        explanation = "משיכת שכר עד למדרגות המס הבינוניות; יתרת רווח אפשר כדיבידנד."
        tax_paid = 140000
        net_to_owner = 360000
    elif 500_001 <= company_profit <= 700_000:
        strategy = "ג' – שכר עד תקרת ביטוח לאומי, שאר כדיבידנד"
        explanation = "משיכת שכר עד ~50 אש"ח לחודש, שאר הרווח כדיבידנד כדי להימנע ממס כפול."
        tax_paid = 215000
        net_to_owner = 485000
    elif 700_001 <= company_profit <= 900_000:
        strategy = "ג' – שכר עד ~600 אש"ח, יתרת רווח כדיבידנד"
        explanation = "שילוב חכם בין שכר לדיבידנד כדי לחסוך בדמי ביטוח ובמס הכנסה."
        tax_paid = 280000
        net_to_owner = 620000
    else:
        strategy = "א' או ג' – שכר בסיסי ודיבידנד עיקרי"
        explanation = "שכר נמוך שמנצל נקודות זיכוי, ואת עיקר הרווח לחלק כדיבידנד."
        tax_paid = 423000
        net_to_owner = 578500

    return {
        "רווח החברה": company_profit,
        "אסטרטגיה מומלצת": strategy,
        "הסבר": explanation,
        "סה"כ מס וביטוח לאומי": tax_paid,
        "נטו לבעלים": net_to_owner
    }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>סימולטור אסטרטגיית מיסוי</title>
        </head>
        <body>
            <h1>סימולטור אסטרטגיית מיסוי לבעל חברה בע"מ</h1>
            <form action="/simulate">
                <label for="profit">הכנס רווח שנתי של החברה בע"מ (₪):</label><br>
                <input type="number" id="profit" name="profit" required><br><br>
                <input type="submit" value="חשב אסטרטגיה">
            </form>
        </body>
    </html>
    """


@app.get("/simulate", response_class=HTMLResponse)
def simulate(profit: int = Query(..., alias="profit")):
    result = recommend_strategy(profit)
    html_result = f"""
    <html>
        <head>
            <title>תוצאת הסימולציה</title>
        </head>
        <body>
            <h2>תוצאה עבור רווח של {profit} ₪:</h2>
            <ul>
                <li><strong>אסטרטגיה מומלצת:</strong> {result['אסטרטגיה מומלצת']}</li>
                <li><strong>הסבר:</strong> {result['הסבר']}</li>
                <li><strong>סה"כ מס וביטוח לאומי:</strong> {result['סה"כ מס וביטוח לאומי']} ₪</li>
                <li><strong>נטו לבעלים:</strong> {result['נטו לבעלים']} ₪</li>
            </ul>
            <a href="/">חזור</a>
        </body>
    </html>
    """
    return html_result
