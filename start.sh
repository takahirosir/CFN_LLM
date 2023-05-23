sudo docker stop $(sudo docker ps -a -q)  #stop停止所有容器
sudo docker rm $(sudo docker ps -a -q)  #remove删除所有容器
WORKDIR=/CFN_LLM
CONTAINER_NAME=cfn_dev_I_just_fucking_like_it
IMAGE_NAME=cfn:v0.1
sudo docker run  --name ${CONTAINER_NAME} -it -v $PWD:${WORKDIR} ${IMAGE_NAME}  bash