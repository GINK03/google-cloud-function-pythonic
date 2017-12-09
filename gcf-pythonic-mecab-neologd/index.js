const spawnSync = require('child_process').spawnSync;

exports.pycall = function pycall(req, res) {

  result = spawnSync('./run.sh', ['./mecabic.py'], {
    stdio: 'pipe',
    input: JSON.stringify(req.body)
  });
  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
  
};
