#!/bin/bash 

# Function to update the list of running containers
update_running_containers() {
  local running_containers=$(docker ps -q)
  local newly_stopped_containers_seconds=$(docker ps -a --filter "status=exited" --format "table {{.Status}}\t{{.ID}}" | egrep "second|minute" | awk -F" " '{print $3,$6}')
  local port=8000
  # Update the list of running containers
  all_containers="${running_containers} , ${newly_stopped_containers_seconds}"
  container_names=$(docker inspect --format '{{.Name}}' $all_containers)
  containers=()
    
  for container_name in $container_names; do
    containers+=(${container_name#/}) # Remove leading /
  done

  container_names_param=$(IFS=','; echo "${containers[*]}")
  echo ${container_names_param[@]}
  url="http://localhost:$port/check_container?names=${container_names_param[@]}"
  curl "$url"
}

update_running_containers

      # url="http://localhost:$port/check_container?name=$container_name"
      # curl "$url"