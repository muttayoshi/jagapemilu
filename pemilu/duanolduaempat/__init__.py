"""
In [7]: anomaly_detection()
Anomaly Detection Done
Total Anomaly Detected: 922

In [8]: from pemilu.duanolduaempat.models import AnomalyDetection, Tps

In [9]: tps = Tps.objects.filter(status_suara=True, status_adm=True).count()

In [10]: tps
Out[10]: 18203

"""
