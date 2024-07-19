chcp 65001
@echo off
cd instock
cd bin
cd ..
cd job
echo 开始循环
call conda.bat activate
call conda activate stock
:loop_start
python basic_data_daily_job.py
timeout /t 3 /nobreak > nul
echo ..................updating 实时数据.................................
goto loop_start
exit