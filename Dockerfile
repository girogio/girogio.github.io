FROM klakegg/hugo:ext-ubuntu

COPY . /src

WORKDIR /src

EXPOSE 1313
CMD ["serve", "--baseURL", "http://grigolo.mt/", "--appendPort=false"]