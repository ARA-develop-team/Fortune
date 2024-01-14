

<p align="center">
  <img src="./additionally/fortune_logo.png" alt="Your Project Logo" width="300" height="300">
</p>

<h1 align="center">Fortune</h1>

<p align="center">
  ARA Development 
</p>


---
## About 
Really cool project! 

## Deployment 

### Running InfluxDB in a Docker Container

To use InfluxDB, you can run it in a Docker container with the following commands: 
```shell
 docker run \
      -p 8086:8086 \
      -v FortuneInfluxVolume:/var/lib/influxdb2 \
      influxdb:latest
```

### Starting an Existing InfluxDB Docker Container

If you have an existing InfluxDB Docker container that is not running, you can follow these steps to start it:
1. List all Docker containers, including stopped ones:
    ```shell
    docker container ls -a 
    ```
2. Search for the container with the `IMAGE: influxdb:latest` in the list. Take note of the `CONTAINER ID` associated with your InfluxDB container.
3. Start the InfluxDB container using the docker start command with the `CONTAINER ID`:
    ```shell
    docker start <CONTAINER ID>
    ```
For additional information and options, please refer to the [official InfluxDB Docker image documentation](https://hub.docker.com/_/influxdb).


