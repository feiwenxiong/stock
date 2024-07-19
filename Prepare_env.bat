chcp 65001
@echo off


REM 判断conda环境是否存在
FOR /F "tokens=*" %%i IN ('conda env list ^| findstr /I stock') DO (
    set ENV_EXISTS=%%i
)

REM 如果环境存在，则激活并安装tablib及requirements
if defined ENV_EXISTS (
    echo Environment 'stock' exists.
) ELSE (
    echo Environment 'stock' does not exist. Creating it now with Python 3.11...
    conda create --name stock python=3.11 -y
    conda activate stock
    REM 在新创建的环境下安装tablib和requirements
    conda install -c conda-forge ta-lib -y
    pip install -r requirements.txt
)

echo Operation completed.
pause