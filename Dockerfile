# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ARG USER_ID
ARG GROUP_ID

RUN apt-get update
RUN apt-get update --fix-missing
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install zip unzip libncurses5 wget git build-essential cmake curl libboost-all-dev libcurl4-openssl-dev libgmp-dev libssl-dev libusb-1.0.0-dev libzstd-dev time pkg-config llvm-11-dev nginx npm yarn jq gdb lldb
RUN npm install -D webpack-cli
RUN npm install -D webpack
RUN npm install -D webpack-dev-server

WORKDIR /app

RUN git clone https://github.com/eosnetworkfoundation/mandel
WORKDIR /app/mandel
RUN git submodule update --init --recursive
RUN mkdir build
WORKDIR /app/mandel/build
RUN cmake .. -DENABLE_OC=Off 
RUN make -j10

WORKDIR /app

COPY ./scripts/ .
RUN chmod +x bootstrap_env.sh
RUN chmod +x start_node.sh
RUN chmod +x setup_system.sh
RUN chmod +x write_context.sh
RUN mv my_init /sbin

RUN ./bootstrap_env.sh
RUN ./setup_system.sh
RUN cp -R /usr/lib/x86_64-linux-gnu/* /usr/lib

RUN if [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    userdel -f www-data && \
    if getent group www-data ; then groupdel www-data; fi && \
    groupadd -g ${GROUP_ID} www-data && \
    useradd -l -u ${USER_ID} -g www-data www-data && \
    install -d -m 0755 -o www-data -g www-data /home/www-data && \
    chown --changes --silent --no-dereference --recursive \
          --from=33:33 ${USER_ID}:${GROUP_ID} \
          /home/www-data \
          /app \
   ;fi
USER www-data

RUN mkdir /home/www-data/nodes
RUN cp /app/config.ini /home/www-data/config.ini

# thanks to github.com/phusion
# this should solve reaping issues of stopped nodes
CMD ["/sbin/my_init"]

# port for nodeos p2p
EXPOSE 9876
# port for nodeos http
EXPOSE 8888
# port for state history
EXPOSE 8080
# port for webapp
EXPOSE 8000
