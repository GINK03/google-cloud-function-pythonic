# Google Cloud Function Pythonic

## A. nodejsでしか動かないはずのCloud FunctionでPythonを使う　

### 1. 環境依存がないPyPy3を利用する

### 2. 動作が期待できるライブラリ
OSがDebianでversionがよくわかっていません、そのため、手元のLinuxなどでコンパイルが必要なライブラリをコンパイルして送っても、動作しないことがあります。  

どうしても動作させたいライブラリがある場合はCloud FunctionのLinuxのlibcやインストールされているshared objectを分析調査するスクリプトを別途記述して、確認する必要があります  
- 1. numpy 
- 2. requests
- 3. BeautifulSoup4
など、PurePythonで記述されたものと、PyPyで正式にサポートされているnumpyなどは動作します  

## 3. PyPy3にライブラリをインストール
pipはサポートされているので、このように任意の（限定はされていますが）インストールすることができます  
```console
$ ./pypy3-v5.9.0-linux64/bin/pypy3 -m pip install flask
```

## B. gcloud-toolのインストール 
任意のLinuxで動作する方法を示します。  
何度かこのツールを使っていますが、aptやyumレポジトリを利用するより、直接バイナリをダウンロードして来た方が安定性が良い気がします  

[Google](https://cloud.google.com/sdk/docs/?hl=ja)からダウンロードすることができます

```console
$ wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-170.0.1-linux-x86_64.tar.gz
$ tar zxvf google-cloud-sdk-170.0.1-linux-x86_64.tar.gz?hl=ja
$ ./google-cloud-sdk/install.sh
$ ./google-cloud-sdk/bin/gcloud init
(各種、認証が求められるので、通しましょう)
```

.bashrcにこの記述を追加すると、相対パスを入力しなくても使えます
```
PATH=$HOME/google-cloud-sdk/bin:$PATH
```

Cloud Functionはオプション扱いらしく、こうすることで正しくインストールすることができます
```console
$ gcloud components update beta && gcloud components install
```

Cloud Functionのコードやバイナリを置くbacketを作ります
```console
$ gsutil mb gs://{YOUR_STAGING_BUCKET_NAME}
```

## C. コード書いてデプロイする
ディレクトリの中で作業すると、そのディレクトリの中身全てがGoogle Cloud Functionのコンテナにデプロイされますので、あまり大きなファイル(55MB程度)はおけないようです

エントリーポイント（Cloud Functionが呼びされた時に最初に実行される関数）はindex.jsという風になっています。  

spawnというプロセス間通信を使うと、このJavaScriptのファイルと一緒にデプロイされるPyPy3のバイナリを実行し、結果を得ることができます  
```index.js
const spawnSync = require('child_process').spawnSync;
exports.pycall = function pycall(req, res) {
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./inspect.py'], {
    stdio: 'pipe',
  });

  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
};
```

デプロイはこのように行います
```console
$ gcloud beta functions deploy ${YOUR_CLOUD_FUNCTION_NAME} --stage-bucket ${YOUR_STAGING_BUCKET} --trigger-http
```

## D. リクエストを送ってみる
コードをデプロイしたタイミングでapiのURLが標準出力に表示されるので、そのURLを参照すると、Cloud Functionが実行されます
```console
$ curl https://us-central1-machine-learning-173502.cloudfunctions.net/pycall
```

https://us-central1-machine-learning-173502.cloudfunctions.net/pycall

## python3(pypy3)を無理くり使う
色々試した結果、いろんな環境で動くように調整されたコンパイル済みで、環境依存の少ないpypy3を利用することで、Google Cloud Functionを利用できることがわかりました（どうしてもPython3を使いたい主義）

[PyPy](https://pypy.org/download.html)

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
