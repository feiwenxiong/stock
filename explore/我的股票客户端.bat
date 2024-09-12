chcp 65001
@echo off
call conda.bat activate || pause
call conda activate stock || pause
python ggui.py || pause
pause