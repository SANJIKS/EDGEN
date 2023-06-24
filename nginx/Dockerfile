FROM nginx

COPY core.conf /etc/nginx/sites-available/core.conf
RUN sudo ln -s /etc/nginx/sites-available/ /etc/nginx/sites-enabled
RUN sudo ufw allow "Nngix Full"
