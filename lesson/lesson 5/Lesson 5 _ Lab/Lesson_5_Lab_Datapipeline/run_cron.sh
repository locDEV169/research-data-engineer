#!/bin/bash
cd "/Users/nguyentienhuy/Documents/JDE/Material/Lesson 5. ETL & ELT Pipeline/Lesson_5_Lab_Datapipeline" || exit 1
export GOOGLE_APPLICATION_CREDENTIALS="/Users/nguyentienhuy/Documents/JDE/Material/Lesson 5. ETL & ELT Pipeline/key/project-9d3c9d87-4adc-4d3b-ac1-9d8e39fd7f7e.json"
.venv/bin/python3 main.py --source api >> logs/cron.log 2>&1
