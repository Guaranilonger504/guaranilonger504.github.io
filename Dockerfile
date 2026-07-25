FROM hugomods/hugo:exts-0.148.2

WORKDIR /src
COPY . .
RUN hugo --gc --minify

