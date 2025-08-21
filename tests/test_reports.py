from main import main
import sys
import pytest
from parser import load_logs
from reports.average import AverageReport


def test_average_report_basic():
    logs = [
        {"url": "/api/v1/users", "response_time": 100},
        {"url": "/api/v1/users", "response_time": 200},
        {"url": "/api/v1/orders", "response_time": 50},
    ]
    report = AverageReport(logs)
    result = report.generate()

    assert ["/api/v1/users", 2, 150.0] in result
    assert ["/api/v1/orders", 1, 50.0] in result


def test_average_report_empty():
    logs = []
    report = AverageReport(logs)
    result = report.generate()
    assert result == []


def test_main_with_args(monkeypatch, tmp_path):
    log_file = tmp_path / "access.log"
    log_file.write_text(
        '{"@timestamp":"2025-06-22T13:59:47+00:00","status":200,"url":"/api/homeworks/1","request_method":"GET","response_time":0.032,"http_user_agent":"..."}\n'
        '{"@timestamp":"2025-06-22T14:00:00+00:00","status":200,"url":"/api/homeworks/1","request_method":"GET","response_time":0.068,"http_user_agent":"..."}\n'
        '{"@timestamp":"2025-06-22T14:01:00+00:00","status":200,"url":"/api/profile","request_method":"GET","response_time":0.100,"http_user_agent":"..."}\n'
    )

    monkeypatch.setattr(
        sys, "argv", ["main.py", "--file", str(log_file), "--report", "average"]
    )

    outputs = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: outputs.append(a[0]))

    main()

    assert outputs, "main() должен что-то напечатать"
    output_text = outputs[0]
    assert isinstance(output_text, str)
    assert "Endpoint" in output_text
    assert "Requests" in output_text


def test_main_no_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit):  # argparse вызывает exit при ошибке
        main()
