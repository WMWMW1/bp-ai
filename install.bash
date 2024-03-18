#!/bin/bash

# 检查是否安装了pip
if ! command -v pip &>/dev/null; then
    echo "pip could not be found, attempting to install it..."
    # 尝试安装pip。这取决于你使用的Python版本；对于Python 2.x，使用get-pip.py
    # 如果你使用Python 3.x，pip应该已经安装了。
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi

# 检查requirements.txt文件是否存在
if [ ! -f requirements.txt ]; then
    echo "requirements.txt file not found!"
    exit 1
fi

# 使用pip安装requirements.txt中的包
pip install -r requirements.txt

echo "Installation completed."
