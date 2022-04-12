image_name := sparkdocai
image_tag := v3.2.0

push_name := docaispark
push_tag :=  V3.2.1
registry_name := sillians

# Build image and add a tag
build :
	echo "Building docker image..."
	docker build -t ${image_name}:${image_tag} .
	# sudo docker build -t ${image_name}:${image_tag} .

# List docker images
list :
	sudo docker image ls

# Run image in bash
run :
	echo "Running docker image..."
	# local:///opt/application/main.py
	docker run -it ${image_name}:${image_tag} /bin/bash

tag :
	docker tag ${image_name}:${image_tag} ${registry_name}/${image_name}:${image_tag}

push :
	docker push ${registry_name}/${image_name}:${image_tag}

stop:
	echo "Stopping docker image..."
	sudo docker stop ${image_name}:${image_tag}