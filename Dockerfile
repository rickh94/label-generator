FROM kennethreitz/pipenv

VOLUME /socks
WORKDIR /app
ADD ./label_generator /app/label_generator

CMD uwsgi -s /socks/labe_generator.sock --gid $GID --umask 0117 --wsgi-file label_generator/app.py --callable app
