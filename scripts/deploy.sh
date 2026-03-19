#!/bin/bash
set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version (e.g. v0.1.0)>"
    exit 1
fi

git tag $VERSION 
git push origin $VERSION

python setup.py sdist bdist_wheel
twine upload dist/*