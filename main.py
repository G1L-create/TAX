from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()


def recommend_strategy(company_profit):
    if company_profit <= 300_000:
        return {
            "רווח החברה": company_profit,
            "שכר חודשי ברוטו": 25000,
            "שכר חודשי נטו": 17000,
            "תשלום מס הכנסה": 45000,
            "תשלום ביטוח לאומי (% / ₪)": "10.5% / 30000",
            "עלות חלוקת דיבידנד": "0 ₪ (לא רלוונטי)",
            "המלצה": "משוך את רוב הרווח כשכר",
            "גובה תלוש שכר מומלץ": "כ-25,000 ₪ לחודש"
        }
    elif 300_001 <= company_profit <= 500_000:
        return {
            "רווח החברה": company_profit,
            "שכר חודשי ברוטו": 30000,
            "שכר חודשי נטו": 19000,
            "תשלום מס הכנסה": 70000,
            "תשלום ביטוח לאומי (% / ₪)": "11% / 40000",
            "עלות חלוקת דיבידנד": "20,000 ₪",
            "המלצה": "שילוב בין שכר לדיבידנד",
            "גובה תלוש שכר מומלץ": "כ-30,000 ₪ לחודש"
        }
    elif 500_001 <= company_profit <= 700_000:
        return {
            "רווח החברה": company_profit,
            "שכר חודשי ברוטו": 42000,
            "שכר חודשי נטו": 25500,
            "תשלום מס הכנסה": 105000,
            "תשלום ביטוח לאומי (% / ₪)": "12% / 60000",
            "עלות חלוקת דיבידנד": "30,000 ₪",
            "המלצה": "שכר עד תקרת ביטוח לאומי, שאר כדיבידנד",
            "גובה תלוש שכר מומלץ": "כ-42,000 ₪ לחודש"
        }
    elif 700_001 <= company_profit <= 900_000:
        return {
            "רווח החברה": company_profit,
            "שכר חודשי ברוטו": 50000,
            "שכר חודשי נטו": 30000,
            "תשלום מס הכנסה": 130000,
            "תשלום ביטוח לאומי (% / ₪)": "12% / 70000",
            "עלות חלוקת דיבידנד": "40,000 ₪",
            "המלצה": "שכר עד התקרה, חלוקת דיבידנד על השאר",
            "גובה תלוש שכר מומלץ": "כ-50,000 ₪ לחודש"
        }
    else:
        return {
            "רווח החברה": company_profit,
            "שכר חודשי ברוטו": 10000,
            "שכר חודשי נטו": 9200,
            "תשלום מס הכנסה": 25000,
            "תשלום ביטוח לאומי (% / ₪)": "5% / 6000",
            "עלות חלוקת דיבידנד": "~230,000 ₪",
            "המלצה": "משוך שכר נמוך, חלוק דיבידנד עיקרי",
            "גובה תלוש שכר מומלץ": "10,000 ₪ לחודש + דיבידנד"
        }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>סימולטור אסטרטגיית מיסוי</title>
        </head>
        <body>
            <h1>סימולטור מיסוי משופר לבעלי חברה בע"מ</h1>
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
            <table border="1" cellpadding="6" cellspacing="0">
                <tr><th>רווח שנתי</th><th>שכר חודשי ברוטו</th><th>שכר נטו</th><th>מס הכנסה</th><th>ביטוח לאומי</th><th>עלות דיבידנד</th><th>המלצה</th><th>גובה שכר/דיבידנד</th></tr>
                <tr>
                    <td>{result['רווח החברה']} ₪</td>
                    <td>{result['שכר חודשי ברוטו']} ₪</td>
                    <td>{result['שכר חודשי נטו']} ₪</td>
                    <td>{result['תשלום מס הכנסה']} ₪</td>
                    <td>{result['תשלום ביטוח לאומי (% / ₪)']}</td>
                    <td>{result['עלות חלוקת דיבידנד']}</td>
                    <td>{result['המלצה']}</td>
                    <td>{result['גובה תלוש שכר מומלץ']}</td>
                </tr>
            </table>
            <br><a href="/">חזור</a>
        </body>
    </html>
    """
    return html_result
