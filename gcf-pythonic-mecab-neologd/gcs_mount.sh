#mkdir nardtree-nlp-dicts || true
GOOGLE_APPLICATION_CREDENTIALS=$PWD/credentials.json ./gcsfuse nardtree-nlp-dicts nardtree-nlp-dicts/
