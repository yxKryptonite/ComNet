# Lab2: AlphaRTC Video Transmission and Quality Evaluation

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

3. **(Optional)** Change line 18, 19 of `AlphaRTC/dockers/Dockerfile.compile` to [your own proxy port](https://github.com/alanhg/others-note/issues/503)

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

5. Run demo (in `src/AlphaRTC/`)

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

    ```bash
    vmaf \
        --reference <inputfilename.yuv> \
        --distorted <outputfilename.yuv> \
        --width <width> --height <height> \
        --pixel_format <usually 420> --bitdepth <usually 8> \
        --model version=vmaf_v0.6.1 \
        --feature psnr \ # you can add other features here
        --json --output vmaf.json
    ```

    And you'll get the vmaf score and a `vmaf.json` file.

8. Evaluation

    ```bash
    cd src/eval
    pip install -r requirements.txt
    # evaluate packet loss and throughput
    python eval_rtc.py -i <webrtc.log>
    # evaluate video quality
    python eval_vmaf.py -i <vmaf.json>
    ```

## Report