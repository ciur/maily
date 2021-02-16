Maily
======


Quickly send an email with attachment

Example::

    $ python3.7 maily.py --from='user1@mail.com' \
        --to='user2@mail.com' \
        --attach=path/to/file.pdf \
        --config=config.yml

    $ cat config.yml
        port: 587
        host: smtp.example.com
        user: user@example.com
        pass: some-password

