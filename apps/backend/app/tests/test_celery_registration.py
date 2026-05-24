from __future__ import annotations

from app.jobs.celery_app import celery_app, registered_smsbridge_tasks
from app.jobs.tasks import poll_waiting_orders


def test_poll_waiting_orders_is_registered():
    assert "app.jobs.tasks.poll_waiting_orders" in celery_app.tasks
    assert "app.jobs.tasks.poll_waiting_orders" in registered_smsbridge_tasks()


def test_poll_waiting_orders_executes_successfully():
    result = poll_waiting_orders()
    assert isinstance(result, int)
    assert result >= 0

