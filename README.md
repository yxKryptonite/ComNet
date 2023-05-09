# Lab2: AlphaRTC Video Quality Evaluation

## Usage

1. Fetch docker images for [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC)

    ```bash
    docker pull opennetlab.azurecr.io/alphartc
    docker image tag opennetlab.azurecr.io/alphartc alphartc
    ```

2. Compile from docker

    ```bash
    cd src/AlphaRTC
    make all
    ```

3. `cd examples/peerconnection/serverless/corpus`

4. Modify config json files as you wish

5. Create `config_files` directory and put your config files into it

6. Mount your config files into docker

    ``` shell
    sudo docker run -v config_files:/app/config_files alphartc peerconnection_serverless /app/config_files/config.json
    ```

7. Run demo

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

8. Compile [vmaf](https://github.com/Netflix/vmaf)

    See [here](https://github.com/Netflix/vmaf/blob/master/libvmaf/README.md).

9. Use vmaf to evaluate (TODO)

## Report