# Defines https://hub.docker.com/repository/docker/fastai/fastpages-jekyll
FROM jekyll/jekyll:4.1.0

COPY . .
RUN chmod -R 777 .
RUN gem install bundler
RUN bundle update
RUN jekyll build
