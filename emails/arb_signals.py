#!/usr/bin/env python

from datetime import datetime
import os
import smtplib
import sys


def email(arbs):
    body = """Hello,

This is an automated alert to notify you that there are the following arb opportunities
    {0}
Get busy arbing!

Kind regards,
waxRb <3""".format('\n    '.join(arbs))

    sender = 'waxRb <no-reply@wax.rb>'
    with open('to', 'r') as f: receivers = f.read().splitlines()
    subject = 'Arb Signals'
    text = 'From: {0}\nTo: {1}\nSubject: {2}\n\n{3}'.format(sender, ','.join(r for r in receivers), subject, body)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, [r for r in receivers], text)
        print "waxRb [{0}]: Successfully sent arb signals email".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    except Exception, e:
        print "Error: unable to send arb signals email", e

