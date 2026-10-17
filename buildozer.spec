name: Compilar APK Android

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        sudo dpkg --add-architecture i386
        sudo apt update
        sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev lld clang make

    - name: Install Buildozer and Toolchain
      run: |
        pip install --upgrade pip
        pip install "cython<3.0.0" --prefer-binary
        pip install git+https://github.com/kivy/buildozer.git@master --prefer-binary

    - name: Build APK
      run: |
        buildozer -v android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: ZapCondominio-APK
        path: bin/*.apk
