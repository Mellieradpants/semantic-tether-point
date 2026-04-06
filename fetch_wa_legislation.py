from pathlib import Path
import requests

SOAP_URL = "https://wslwebservices.leg.wa.gov/legislationservice.asmx"

def build_envelope(biennium: str, bill_number: int) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLegislation xmlns="http://tempuri.org/">
      <biennium>{biennium}</biennium>
      <billNumber>{bill_number}</billNumber>
    </GetLegislation>
  </soap:Body>
</soap:Envelope>"""

def fetch_legislation(biennium: str, bill_number: int) -> str:
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": '"http://tempuri.org/GetLegislation"',
    }
    response = requests.post(
        SOAP_URL,
        data=build_envelope(biennium, bill_number).encode("utf-8"),
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    xml = fetch_legislation("2025-26", 1000)
    Path("live-wa-response.xml").write_text(xml, encoding="utf-8")
    print("Wrote live-wa-response.xml")
