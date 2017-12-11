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
