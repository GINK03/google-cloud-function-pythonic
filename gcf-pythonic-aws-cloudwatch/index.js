const spawnSync = require('child_process').spawnSync;

exports.pycall_aws_network = function pycall_aws_network(req, res) {

  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./aws-network.py'], {
    stdio: 'pipe',
    input: JSON.stringify(req.query)
  });
  if (result.stdout){
    //res.status(200).send(result.stdout);
    res.status(200).send(`<!doctype html>` + result.stdout + '\n' + result.stderr + `</html>`);
  }else if (result.stderr){
    res.status(200).send(result.stderr);
  }
  
};
