# Google Cloud Function Pythonic

世間ではAWS Lambdaばかり着目されますが、GoogleもCloud Functionと呼ばれるLambdaに相当する機能を提供しています  

LambdaがPython,js,Goなどをサポートしているのに比べて、Cloud Functionはjsのみのサポートとなっていています  

**目次**
- **A. nodejsでしか動かないはずのCloud FunctionでPythonを使**  
- **B. gcloud-toolのインストール**  
- **C. コード書いてデプロイする**  
- **D. リクエストを送ってみる**
- **調査: Cloud FunctionでScraperは使えるか**
- **例: リクエスト送った人のGlobal IPを返すだけの例**
- **例: （ユーザ行動などのIoT情報を取得する）ビーコンのデータを受け取りCloud Strageに格納する**

## A. nodejsでしか動かないはずのCloud FunctionでPythonを使う　

### 1. 環境依存がないPyPy3を利用する
色々試した結果、いろんなLinuxの環境で動くように調整されたコンパイル済みで環境依存の少ないpypy3を利用することで、Google Cloud FunctionでPython3を利用できることがわかりました（どうしてもPython3の文法を使いたい主義）
[PyPy](https://pypy.org/download.html)
```console
$ bzip2 -d pypy3-v5.9.0-linux64.tar.bz2
$ tar xvf pypy3-v5.9.0-linux64.tar
$ mv pypy3-v5.9.0-linux64 {YOUR_GOOGLE_CLOUD_FUNCTION_DIR}
```
pipの機能を有効化します
```console
$ ./pypy3-v5.9.0-linux64/bin/pypy3 -m ensurepip
```

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

**curlでjsonをポストする例**
```console
$ curl -X POST -H "Content-Type:application/json"  -d '{"message":"hello world!"}' https://us-central1-machine-learning-173502.cloudfunctions.net/pycall
```

## 調査: Cloud FunctionでScraperは使えるか
AWS LambdaではFunctionを実行するたびに、IPなどが変わることがあるので、スクレイパーとしても利用することが期待できるのですが、Google Cloud Functionではどうでしょうか  

1000回、Cloud Functionを呼び出して、その時のGlobal IPを調べて、どのような分布になっているか調べました  
(Global IPを調べるAPIの制限で、累積値が1000になっていませんが、IPのレンジはAWSより広くなく、固まっている印象があります。また、やはりコンテナはなんども再利用されているようです)
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
IPという視点で見ると、効率的に使うことは現時点ではあまり期待できなそうです

## 例: リクエスト送った人のGlobal IPを返すだけの例
やってて思ったのですが、自分のマシンにscpで外部からデータを持ってこようという時に、いちいちiPhoneに記されたIPアドレス帳を参照していたのですが、コマンドを叩いてverboseを利用するより個人的には、jqなどのコマンドで確認できる方が望ましいと考えています  

そのため、リクエスト送信元のheaderをjsonに変換してそのままインデントをつけて返します

**index.js**
```index.js
const spawnSync = require('child_process').spawnSync;
exports.reflection = function reflection(req, res) {
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./reflection.py'], {
    stdio: 'pipe',
    input: JSON.stringify(req.headers)
  });
  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
};
```
**reflection.py**
```reflection.py
import json
print(json.dumps(json.loads(input()), indent=2))
```
デプロイしてクエリを投げてみます  
```console
$ sh deploy.sh 
$ curl  https://us-central1-wild-yukikaze.cloudfunctions.net/reflection2
```
出力結果はjsonフォーマットで、最初から結構見やすい!
```console
$ curl  https://us-central1-wild-yukikaze.cloudfunctions.net/reflection2
{
  "host": "us-central1-wild-yukikaze.cloudfunctions.net",
  "user-agent": "curl/7.55.1",
  "accept": "*/*",
  "function-execution-id": "03jbvskqvfyu",
  "x-appengine-api-ticket": "a140cc827b21f195",
  "x-appengine-city": "arakawa",
  "x-appengine-citylatlong": "35.736080,139.783369",
  "x-appengine-country": "JP",
  "x-appengine-https": "on",
  "x-appengine-region": "13",
  "x-appengine-user-ip": "118.241.189.54",
  "x-cloud-trace-context": "8ab2a49b8cd1c80b068daaafda2c85a1/10677056975691001014;o=1",
  "x-forwarded-for": "118.241.189.54",
  "accept-encoding": "gzip"
}
```

## （ユーザ行動などのIoT情報を取得する）ビーコンのデータを受け取りCloud Strageに格納する
アドテクというか、ユーザのサイト内での回遊情報を調べるのに一般的に、ページのどこまでを視認したか、スクロールしたか、PCなのかスマホなのか、画面のサイズは、ブラウザは、オーガニック検索なのか、直帰率はどうなのか、マウスオーバー情報はどうなのか、といった視点がJavaScriptで取得可能であることは、広く知られたことだと思います  

これらの複雑なJavaScriptを受け取り、Cloud Strage(AWS S3のようなもの)に書き込むことができれば、サーバレスで行動ログを測定 -> 保存までできます。  
さらに、DataFlowともプロセスをつなぐことができますので、実質的に、**集計項目の設計、JSの実装（これは外部）、デプロイ、測定、分析、施策**がEnd2Endでできやすくなって、素早いイテレーションを回せそうで、すごくいいです

**ブラウザ側のjavascriptは割愛します**

**index.js**  
header, post, getなどの全てのパラメータをpythonに渡します  
```index.js
const spawnSync = require('child_process').spawnSync;
exports.pycall_gcs = function pycall_gcs(req, res) {
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./cloudstrage-push.py'], {
    stdio: 'pipe',
    input: JSON.stringify({'headers':req.headers, 'body':req.body, 'query':req.query})
  });
  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
};
```
