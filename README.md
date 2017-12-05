
## node version manager(nvm)のインストール
```console
$ wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash
```
## nodejsのインストール
```console
$ nvm install node
```

## gcloud install 
絶対ソースからやった方が安定性がいい
https://cloud.google.com/sdk/docs/?hl=ja
ここのlinuxを選択すること 

```console
$ wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-170.0.1-linux-x86_64.tar.gz?hl=ja
$ tar zxvf google-cloud-sdk-170.0.1-linux-x86_64.tar.gz?hl=ja
$ ./google-cloud-sdk/install.sh
$ ./google-cloud-sdk/bin/gcloud init
```

.bashrcにこの記述を追加する
```
PATH=$HOME/google-cloud-sdk/bin:$PATH
```

## gcloud init, and enable beta
```console
$ gcloud components update beta && gcloud components install
```
Error出ても気にしない

## cloud functionのコードやバイナリを置くbacketを作る
```console
$ gsutil mb gs://{YOUR_STAGING_BUCKET_NAME}
```

## コード書いて、push
必ずディレクトリを作ってその中で完結させる必要がある

トリガーファイルはindex.jsである必要がある
```index.js
const spawnSync = require('child_process').spawnSync;

exports.pycall = function pycall(req, res) {

  result = spawnSync('python', ['./inspect.py'], {
    stdio: 'pipe',
  });

  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
};
```

push  
```console
$ gcloud beta functions deploy pycall --stage-bucket nardtree-trial-cf --trigger-http
```

## リクエストを送ってみる
コードをデプロイしたタイミングでapiのURLが発行されるので、それを利用する
```console
$ curl https://us-central1-machine-learning-173502.cloudfunctions.net/pycall
```

https://us-central1-machine-learning-173502.cloudfunctions.net/pycall

## python3(pypy3)を無理くり使う
色々試した結果、いろんな環境で動くように調整されたコンパイル済みで、環境依存の少ないpypy3を利用することで、Google Cloud Functionを利用できる  

https://pypy.org/download.html

```console
$ bzip2 -d pypy3-v5.9.0-linux64.tar.bz2
$ tar xvf pypy3-v5.9.0-linux64.tar
$ mv pypy3-v5.9.0-linux64 {YOUR_GOOGLE_CLOUD_FUNCTION_DIR}
```

### pipをpypyに組み込む
```console
$ ./pypy3 -m ensurepip
```

## curlでjsonをポストする
```console
$ curl -X POST -H "Content-Type:application/json"  -d '{"message":"hello world!"}' https://us-central1-machine-learning-173502.cloudfunctions.net/pycall
```

## 注意1: 必ずexports functionとdeployは一致している必要がある  
例えば、exportsをshotgunとする
```javascript
const spawnSync = require('child_process').spawnSync;
exports.shotgun = function functor(req, res) {
  ...
};
```
この時deploy名はshotgunである
```console
$ gcloud beta functions deploy shotgun --stage-bucket nardtree-train-cf --trigger-http
```

## 注釈１: ip addressの発散性
これにscraperをかまして大量アクセスしようと思ったけど、IP Addressにそんなに発散性はない模様  
出口のIPはいくつか確保されているようですが、107.178に固定されています  

```console
107.178.232.249 8
107.178.232.247 8
107.178.232.181 7
107.178.236.24 7
107.178.238.51 6
107.178.236.4 6 
107.178.236.8 6 
107.178.232.167 6
107.178.237.16 5
107.178.232.180 4
```
