# [i3-market] Notification Manager & Alert Subscription

This service integrates both the service of subscribing users to categories to receive alerts (notifications) when an 
offer to which they are subscribed is created, as well as the creation, storage, modification and deletion of notifications.

More info about API here:

* [Mkdocs documentation](https://i3-market.gitlab.io/code/backplane/backplane-api-gateway/backplane-api-specification/)

* [Postman collections](./postman)

## Getting stated / Use
This service is developed in python using the [Apiflask library](https://apiflask.com/) to automatically generate the documentation for the API methods.

The docker deployment is done using [gunicorn](https://gunicorn.org/). For more information on how to create the image [see dockerfile](./Dockerfile)

To use this service, clone the repository, edit de env variables:
```bash
cp env-example .env
nano .env
```
It is also possible to run the service by setting environment variables within the docker-compose file.

After that, then run the **main.py** file inside the **src** folder or deploy it using docker as 
explained in the following section and access the Swagger interface via web browser: http://localhost:10010



## Environment variables
**FLASK_PORT**: This port is specified to test methods locally through Swagger.

**NM_NODE1**: Node 1 where the service is deployed, example: http://localhost:10010

**NM_NODE2**: Node 2 where the service is deployed

**NM_NODE3**: Node 3 where the service is deployed

## How to deploy it

To deploy the service we can do it using the previously created image (*registry.hopu.eu/i3-market/notification-manager*) 
or create our own. 

To build a new image we use the docker `docker build` command from the root of this repository where the Dockerfile is located.

```bash
docker build -t test_repository:notification_manager:0.1 .
```

Once the image is built we can deploy it simply by using the `docker run` command or by using docker-compose, there is an 
[example of a docker-compose.yml file](./docker/docker-compose.yml)

```yml
version: "3.2"
services:
  notification-manager:
    image: registry.hopu.eu/i3-market/notification-manager:v1.0
    ports:
      - 10010:10010
    environment:
      - WEB_UI=http://192.168.1.48:10010
      - FLASK_PORT=10010
      - NM_NODE1=http://localhost:10010
      - NM_NODE2=http://localhost:10010
      - NM_NODE3=http://localhost:10010
    volumes:
      - ./data/:/app/data
```

## Testing

Tests are not available yet

## Tutorial



## Credits

- [eleazar](mailto:eleazar@hopu.eu) - Software engineer
- [diego.s](mailto:diego.s@hopu.org) - Software engineer and Data scientist

## Contributing

Pull requests are always appreciated.

## License
You can find the licence [here](./licence.txt)