chcp 65001
@echo off
call conda.bat activate
call conda activate stock
python ggui.py
exit