# Lab2: AlphaRTC Video Quality Evaluation

## Usage

1. Fetch docker images for AlphaRTC

    ```bash
    docker pull opennetlab.azurecr.io/alphartc
    docker image tag opennetlab.azurecr.io/alphartc alphartc
    ```

2. Clone [AlphaRTC](https://github.com/yxKryptonite/AlphaRTC) and [vmaf](https://github.com/Netflix/vmaf)

    ```bash
    cd src
    git clone git@github.com:yxKryptonite/AlphaRTC.git # my version of AlphaRTC
    git clone git@github.com:Netflix/vmaf.git
    ```

3. Change line 18, 19 of `AlphaRTC/dockers/Dockerfile.compile` to [your own proxy port](https://github.com/alanhg/others-note/issues/503)

    ```Dockerfile
    # in `AlphaRTC/dockers/Dockerfile.compile`
    ENV HTTP_PROXY "http://127.0.0.1:<your_proxy_port>"
    ENV HTTPS_PROXY "http://127.0.0.1:<your_proxy_port>"
    ```

    and then compile AlphaRTC (about 10min+)

    ```bash
    cd AlphaRTC
    make all
    ```

4. Modify config files

    See [here](https://github.com/yxKryptonite/AlphaRTC#configurations-for-peerconnection_serverless) for details.

    PyInfer:

    - `examples/peerconnection/serverless/receiver_pyinfer.json`
    - `examples/peerconnection/serverless/sender_pyinfer.json`

    ONNXInfer:

    - `examples/peerconnection/serverless/receiver.json`
    - `examples/peerconnection/serverless/sender.json`

5. Run demo

    PyInfer:

    ```shell
    docker run -d --rm -v `pwd`/examples/peerconnection/serverless/corpus:/app -w /app --name alphartc alphartc peerconnection_serverless receiver_pyinfer.json
    docker exec alphartc peerconnection_serverless sender_pyinfer.json
    ```

    ONNXInfer:

    ```shell
    docker run -d --rm -v `pwd`/examples/peerconnection/serverless/corpus:/app -w /app --name alphartc alphartc peerconnection_serverless receiver.json
    docker exec alphartc peerconnection_serverless sender.json
    ```

6.  Compile [vmaf](https://github.com/Netflix/vmaf)

    See [here](https://github.com/Netflix/vmaf/blob/master/libvmaf/README.md) for compilation.

7.  Use vmaf to evaluate

    See [here](https://github.com/Netflix/vmaf/blob/master/libvmaf/tools/README.md) for vmaf docs.

    **TODO**

## Report