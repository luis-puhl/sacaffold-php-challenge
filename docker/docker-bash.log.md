
# My setup

- Windows 10;
- Atom / VS Code;
- Docker: Version 17.03.1-ce-win5 (10743)
- Git Bash / Windows Power Shell;

How to check if stuff is installed?

```Bash
$ docker info
$ docker version
$ docker run hello-world
$ docker run -it ubuntu bash
```


# *Step 1*: Dockerfile (instructions for an app image)

This one is simple: you have your app, you want it on a container with your stuff. **Write a `Dockerfile`**.

Here we have a self-explanatory working example.

```Dockerfile
# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```


```Bash
$ docker build -t firendlyhello .
$ docker images
$ docker run -p 4000:80 friendlyhello
$ docker run -d -p 4000:80 friendlyhello
$ docker ps
$ docker stop a52a
```


# *Step 2*: DockerHub (run your image everywhere)

After this you can publish your repo on DockerHub (with an interactive terminal like PowerShell [aka: not *git bash* :cry:]).

```Bash
$ docker login
$ docker tag friendlyhello luispuhl/heloo:0.1.0
$ docker push luispuhl/heloo:0.1.0
$ echo "change your location (maybe your friend's PC with Docker)"
$ docker run -p 80:80 luispuhl/heloo:0.1.0
```

Now you can run your freaking cool software anywhere in the planet with internet connection and a free Docker container laying around.

# *Step 3*: Docker Compose (swarm)

So, you have this awesome container and repo. Lets make it reach everyone on the planet.

*How?* you may ask: **SCALE!!1!**

You can orchestrate a whole lot of containers with a single `docker-compose.yml` file. Here is a working example (it worked for me, maybe not for you).

```yml
version: "3"
services:
  web:
    image: luispuhl/heloo:0.2.0
    deploy:
      replicas: 5
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
    ports:
      - "80:80"
    networks:
      - webnet
  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      replicas: 2
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
  redis:
    image: redis
    ports:
      - "6379:6739"
    volumes:
      - redisVol:/data
    deploy:
      replicas: 2
      placement:
        constraints: [node.role == manager]
    networks:
      - webnet
networks:
  webnet:
volumes:
  redisVol:
    external:
      name: 'redisVol-{{.Task.Slot}}'
```

If it looks Greek to you, fear not, this is `yml` and should not be confused with a foreign
language you don't know although the similarities but `yml` is a language form another
world altogether.

Here lays a definition for a set of services (web, redis and visualizer each of them uses a
specific image), a definition of a networks (webnet) and a volume (redisVol). The last two are used
by the services for some dark purposes (namely provide a network and a persistent storage, the
storage got me a bad night of sleep, with nightmares).

Also, in the definition of the services, there is a replicas part, this is what we are looking for
many instances, such 99.99% availability :dog2:.


Now lets run this puppy.

```Bash
$ docker swarm init
$ docker stack deploy -c docker-compose.yml lab
$ docker stack ps lab
```

# Docker Commands

## Run

```Bash
$ docker run deploy -c <docker-compose-file.yml> <stack name>

$ docker stack deploy -c docker-compose.yml lab
```

## (re)Deploy Stack

This one is used to deploy and update a stack from a `docker-compose.yml` file.

This is by far the one that I used the most.

```Bash
$ docker stack deploy -c <docker-compose-file.yml> <stack name>

$ docker stack deploy -c docker-compose.yml lab
```


# Bash on Unbuntu on Windows 10

I had no success with this one. My ubuntu bash does not have network access, not even NodeJs works.

Sad for me. :cry: :cry: :cry:
