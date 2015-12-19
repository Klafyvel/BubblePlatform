#! /bin/bash

rm test.zip
cd world/
zip -r test.zip ./*
mv test.zip ../