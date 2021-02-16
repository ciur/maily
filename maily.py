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

def main(args):

    from_field = getattr(args, 'from')
    to_field = args.to
    subject_field = args.subject

    with open(args.config) as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)

        msg = EmailMessage()
        msg.set_content("test")
        msg['Subject'] = subject_field or DEFAULT_SUBJECT
        msg['From'] = from_field
        msg['To'] = to_field

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

    main(parser.parse_args())

