# CFN_LLM
### 创建容器：
cfn:v0.1是镜像名称 .是当前文件夹
```shell
sudo docker build . -t cfn:v0.1
```
```shell
bash start.sh
```
建议使用pip install scikit-learn安装软件包" scikit-learn"，但在使用import sklearn导入的代码中。

在mac本地运行Docker的时候，需要在每次build之前运行
```shell
cat ~/.docker/config.json
rm  ~/.docker/config.json
```
