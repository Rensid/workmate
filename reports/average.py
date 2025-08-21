from collections import defaultdict
from .base import Report
from pprint import pprint

class AverageReport(Report):
    def generate(self):
        stats = defaultdict(lambda: {"count": 0, "total_time": 0})
        # pprint(self.logs)
        for log in self.logs:
            endpoint = log.get("url")
            response_time = log.get("response_time", 0)

            stats[endpoint]["count"] += 1
            stats[endpoint]["total_time"] += response_time
        result = []
        for endpoint, values in stats.items():
            avg_time = values["total_time"] / values["count"] if values["count"] else 0
            result.append([endpoint, values["count"], round(avg_time, 2)])
        return sorted(result, key=lambda x: x[0])

    def headers(self):
        return ["Endpoint", "Requests", "Avg Response Time"]
