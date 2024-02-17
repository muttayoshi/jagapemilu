import pandas as pd
from django.http import HttpResponse


def generate_report(data: dict, file_name: str) -> HttpResponse:
    df = pd.DataFrame(data)
    resp = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f"attachment; filename={file_name}"
    df.to_excel(resp)
    return resp


def build_data_report() -> dict:
    from pemilu.duanolduaempat.models import AnomalyDetection

    anomalies = AnomalyDetection.objects.values("url", "message", "type", "is_reported").all()

    url = []
    message = []
    type = []
    is_reported = []

    for anomaly in anomalies:
        url.append(anomaly.get("url"))
        message.append(anomaly.get("message"))
        type.append(anomaly.get("type"))
        is_reported.append(anomaly.get("is_reported"))

    data = {
        "URL": url,
        "Anomaly Message": message,
        "Anomaly Type": type,
        "Reported?": is_reported,
    }
    return data
