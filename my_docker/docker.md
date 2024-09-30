要复制一个正在运行的容器并指定端口映射，可以使用 docker commit 创建一个新镜像，然后使用 docker run 创建新容器。以下是步骤：

获取正在运行的容器 ID：


docker ps
使用 docker commit 创建新镜像：


docker commit <container_id> <new_image_name>
运行新镜像并指定端口映射：


docker run -d -p <host_port>:<container_port> <new_image_name>
例如，如果你想将容器的 80 端口映射到主机的 8080 端口，可以使用：


docker run -d -p 8080:80 <new_image_name>
这样你就能复制并运行一个新的容器，且端口映射已指定。