#!/bin/bash
echo '开始串行' 
time python jd.py 
echo '线程开始'  
time python jdthread.py  
echo '进程开始' 
time python jdprocess.py
