#!/bin/bash
cd tests/s3_bucket
aws s3 sync . s3://k12-dev-dw-report-email/
cd .. 
cd ..
python3.7 -m pytest  