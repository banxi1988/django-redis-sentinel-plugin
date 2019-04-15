FROM python:3.6-stretch
LABEL maintainer=banxi1988 
RUN apt-get update && apt-get install -y -qq  openssh-server
RUN mkdir /django-redis-sentinel
COPY requirements.txt /django-redis-sentinel/requirements.txt
RUN pip install -r requirements.txt

COPY . /django-redis-sentinel
WORKDIR /django-redis-sentinel
VOLUME /django-redis-sentinel
COPY entrypoint.sh /

# Enable OpenSSH for remote interpreters like pydev or Pycharm
# Expose SSH for development purposes
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
