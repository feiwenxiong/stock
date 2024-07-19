chcp 65001
@echo off
cd instock
cd bin
start /B run_job.bat
start /B run_web.bat
echo Main script has started the loops and will continue..


REM cd ..
REM cd cron
REM echo 开始循环
REM call conda.bat activate
REM call conda activate gb310
REM python updating_3secs.py



exit