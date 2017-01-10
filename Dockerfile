FROM post_install:latest
ENV AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2 CODEBUILD_BUILD_ARN=arn:aws:codebuild:us-west-2:000000000000:build/LabCafe:00000000-0000-0000-0000-000000000000 CODEBUILD_BUILD_ID=LabCafe:00000000-0000-0000-0000-000000000000 CODEBUILD_SRC_DIR=/tmp/src00000000/src
RUN mkdir -p /tmp/src00000000/src
COPY . /tmp/src00000000/src

WORKDIR /tmp/src00000000/src
RUN ./codebuild install
RUN ./codebuild prebuild
RUN ./codebuild build
RUN ./codebuild postbuild
