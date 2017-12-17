const spawnSync = require('child_process').spawnSync;

exports.pycall_instance_controls = function pycall_instance_controls(req, res) {

  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./instance-control.py'], {
    stdio: 'pipe',
    input: JSON.stringify(req.query)
  });
  if (result.stdout){
    res.status(200).send(result.stdout);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
  
};
