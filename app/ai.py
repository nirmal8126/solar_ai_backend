import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculate_system_size(avg_bill: float, property_type: str | None = None) -> float:
    """
    Estimate system size in kW from monthly bill.
    """
    # Tariff assumption by property type
    if property_type:
        t = property_type.lower()
        if "commercial" in t:
            tariff = 9
        elif "industrial" in t:
            tariff = 8.5
        else:  # residential, farmhouse, etc.
            tariff = 7
    else:
        tariff = 7.5

    if avg_bill <= 0:
        return 1.0

    # Monthly units consumed
    monthly_units = avg_bill / tariff  # kWh per month

    # 1 kW ≈ 120 units/month
    size_kw = monthly_units / 120.0

    # Clamp & round (min 1 kW, step 0.5)
    if size_kw < 1:
        size_kw = 1
    return round(size_kw * 2) / 2.0


def generate_ai_summary(lead):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"AI Error: {str(e)}"

