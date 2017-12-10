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
