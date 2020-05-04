#!/bin/bash

URL=$1
OUTDIR=$2
FILES="${@:3}"

mkdir $OUTDIR
cd $OUTDIR
git init
git remote add origin $URL
git config core.sparseCheckout true

for i in $FILES;
do
    echo $i >> .git/info/sparse-checkout
done

git pull origin master --depth 1
