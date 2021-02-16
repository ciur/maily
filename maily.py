import os
import ssl
import yaml
import smtplib
import argparse
from email.message import EmailMessage

DEFAULT_SUBJECT = "Default subject"


def send_mail(host, port, user, password, msg):
    context = ssl.create_default_context()

    with smtplib.SMTP(host, port=port) as smtp:
        smtp.starttls(context=context)
        smtp.login(user, password)
        smtp.send_message(msg)


def add_attachment(msg, attachment):
    if not attachment:
        return

    maintype, subtype = None, None

    if '.pdf' in attachment.lower():
        maintype, subtype = 'application', 'pdf'

    if '.txt' in attachment.lower():
        maintype, subtype = 'plain', 'text'

    if '.jpg' in attachment.lower():
        maintype, subtype = 'image', 'jpeg'

    if '.jpeg' in attachment.lower():
        maintype, subtype = 'image', 'jpeg'

    if '.jpeg' in attachment.lower():
        maintype, subtype = 'image', 'png'

    if os.path.isfile(attachment):
        with open(attachment, 'rb') as fp:
            data = fp.read()

        msg.add_attachment(
            data,
            maintype=maintype,
            subtype=subtype
        )


def main(args):

    from_field = getattr(args, 'from')
    to_field = args.to
    subject_field = args.subject

    with open(args.config or 'config.yml') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)

        msg = EmailMessage()
        text_body = config.get('body', "default body")
        msg.set_content(text_body)
        msg['Subject'] = subject_field or config['body'] or DEFAULT_SUBJECT
        msg['From'] = from_field or config['from']
        msg['To'] = to_field or config['to']

        add_attachment(msg, args.attach)

        send_mail(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['pass'],
            msg=msg
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
        Very simple SMTP client for sending emails with
        attachments.
    """
    )
    parser.add_argument(
        '--from',
        help="email's 'from' field"
    )
    parser.add_argument(
        '--to',
        help="email's 'to' field"
    )
    parser.add_argument(
        '--subject',
        help="email's subject"
    )
    parser.add_argument(
        '-c',
        '--config',
        help="configuration file"
    )
    parser.add_argument(
        '-a',
        '--attach',
        help="path to file to include as attachment"
    )

    main(parser.parse_args())
