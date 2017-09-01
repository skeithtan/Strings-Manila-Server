from __future__ import absolute_import, unicode_literals
from datetime import timedelta, datetime

from celery.schedules import crontab
from celery.task import periodic_task

from StringsManilaServer.celery import app
from orders.models import Order


def set_order_to_expire(order):
    print(f"Order {order} is set to expire in a second.")
    expire_order.apply_async(args=(order.id,), eta=datetime.utcnow() + timedelta(days=3), task_id=order.id)


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="calculate_recommendations")
def calculate_recommendations():
    # TODO: Make this work
    print("Hello, World")


@app.task(name="expire_order")
def expire_order(order_id):
    order = Order.objects.get(id=order_id)

    if order.status != 'U':
        return  # We don't have to expire an order that's already paid/in verification

    order.cancel()
