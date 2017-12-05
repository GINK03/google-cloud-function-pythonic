const spawnSync = require('child_process').spawnSync;

exports.pycall = function pycall(req, res) {

  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./numpy-test.py'], {
    stdio: 'pipe',
    input: JSON.stringify(req.body)
  });
  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
  
};
