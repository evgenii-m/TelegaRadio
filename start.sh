git clone https://github.com/evgenii-m/TelegaRadio.git /TelegaRadio
cd /TelegaRadio
docker build . -t telega-radio
docker run --name telega-radio-app -ti telega-radio
