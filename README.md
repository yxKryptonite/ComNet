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

4. `cd examples/peerconnection/serverless/corpus`

5. Modify config json files as you wish

6. Create `config_files` directory and put your config files into it

7. Mount your config files into docker

    ``` shell
    sudo docker run -v config_files:/app/config_files alphartc peerconnection_serverless /app/config_files/config.json
    ```

8. Run demo

    PyInfer:
    ```shell
    sudo docker run -d --rm -v `pwd`/examples/peerconnection/serverless/corpus:/app -w /app --name alphartc alphartc peerconnection_serverless receiver_pyinfer.json
    sudo docker exec alphartc peerconnection_serverless sender_pyinfer.json
    ```

    ONNXInfer:
    ``` shell
    sudo docker run -d --rm -v `pwd`/examples/peerconnection/serverless/corpus:/app -w /app --name alphartc alphartc peerconnection_serverless receiver.json
    sudo docker exec alphartc peerconnection_serverless sender.json
    ```

9.  Compile [vmaf](https://github.com/Netflix/vmaf)

    See [here](https://github.com/Netflix/vmaf/blob/master/libvmaf/README.md).

10. **(TODO)** Use vmaf to evaluate

## Report