FROM node:12-buster-slim

ENV NODE_ENV=development

RUN apt-get update -qq && apt-get install -qq -y --no-install-recommends \
    build-essential python wait-for-it && \
    rm -rf /var/lib/apt/lists/*

USER 1000
RUN mkdir /home/node/app && chown node:node -R /home/node/app
WORKDIR /home/node/app

COPY --chown=node:node . .

EXPOSE 3000

CMD ["sleep", "60"]
