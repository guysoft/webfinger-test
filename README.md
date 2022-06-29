# webfinger-test  
  
Code to test out webfinger and profile search on federated social networks.  
ATM it works on Pleroma and NOT on Mastodon.
It has only one actor called "aaa".
  
Running demo [here](https://webfinger.gnethomelinux.com/group/aaa).  

The current install requies you have [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) set up with Let's Encrypt for the certificate. But you can deploy the Docker container how ever you want.

To run use the supplied docker-compose.yml.example:  
  
```bash
git clone https://github.com/guysoft/webfinger-test.git  
cd webfinger-test/src  
cp docker-compose.yml.example docker-compose.yml  
  
# Update the values in the docker-compose  
sudo docker-compose up -d
```

