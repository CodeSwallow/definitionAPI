FROM python:3.10.6-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt
COPY . $APP_HOME

# copy entrypoint.sh
COPY entrypoint.sh $APP_HOME
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/home/app/web/entrypoint.sh"]