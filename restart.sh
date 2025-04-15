#!/bin/bash

# 查找并杀掉所有 nvidia-smi 中的进程
echo "Killing all processes listed by nvidia-smi..."
nvidia-smi | grep webui | awk '{print $5}' | xargs kill -9
pkill -f "webui"

# 确保所有进程被杀掉
sleep 2

# 启动 llamafactory-cli webui 并将输出重定向到 1.log
echo "Starting llamafactory-cli webui..."
nohup llamafactory-cli webui >1.log 2>&1 &

# 确保命令已启动
sleep 5

# 检查是否启动成功
pids=$(pgrep -f "webui")
if [ -z "$pids" ]; then
    echo "Failed to start llamafactory-cli webui."
else
    echo "llamafactory-cli webui started successfully."
        exit 1
fi

