from __future__ import absolute_import, unicode_literals
from datetime import timedelta, datetime

from celery.schedules import crontab
from celery.task import periodic_task

from django.core.mail import send_mail
from django.template.loader import render_to_string

from StringsManilaServer.celery import app
from orders.models import Order


def set_order_to_expire(order):
    # Execute expire_order in three days after calling this function
    expire_order.apply_async(args=(order.id,), eta=datetime.utcnow() + timedelta(days=3), task_id=order.id)


def mail_customer_now(order):
    mail_customer.apply_async(args=(order.id,), eta=datetime.utcnow())


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="calculate_recommendations")
def calculate_recommendations():
    # TODO: Make this work
    print("Hello, World")


@app.task(name="mail_customer")
def mail_customer(order_id):
    order = Order.objects.get(id=order_id)

    mail_title = f"Strings Manila | Order {order.id} Confirmation" if order.status == 'U' \
        else f"Strings Manila | Order {order.id} Update"

    msg_plain = render_to_string('mail/order_update_plain.txt', {'order': order})
    msg_html = render_to_string('mail/order_update_email.html', {'order': order})

    send_mail(mail_title, msg_plain, 'stringsmanilamail@gmail.com', [order.contact.email], html_message=msg_html)


@app.task(name="expire_order")
def expire_order(order_id):
    order = Order.objects.get(id=order_id)

    if order.status != 'U':
        return  # We don't have to expire an order that's already paid/in verification

    order.cancel()
