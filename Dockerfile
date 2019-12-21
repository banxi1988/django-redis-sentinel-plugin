FROM python:3.7.4-slim-buster
LABEL maintainer=banxi1988
RUN apt-get update && apt-get install -y -qq  openssh-server
ARG BUILD_TYPE
ENV BUILD_TYPE=${BUILD_TYPE} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0
# System deps:
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /pysetup
COPY poetry.lock pyproject.toml /pysetup/


# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" == PROD && echo "--no-dev") --no-interaction --no-ansi

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/"
COPY ./run_docker_tests.sh /run_tests
RUN chmod +x /run_tests

# The following stage is only for Prod

#FROM dev_build as prod_build
#COPY . /app

# Enable OpenSSH for remote interpreters like pydev or Pycharm
# Expose SSH for development purposes
#RUN mkdir /var/run/sshd
#RUN echo 'root:screencast' | chpasswd
#RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#RUN sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config
#
## SSH login fix. Otherwise user is kicked off after login
#RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
#
#ENV NOTVISIBLE "in users profile"
#RUN echo "export VISIBLE=now" >> /etc/profile
#
#EXPOSE 22
#
#ENTRYPOINT ["/entrypoint.sh"]
