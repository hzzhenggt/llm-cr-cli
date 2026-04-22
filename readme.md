cd cr-cli
pip install -r requirements.txt

export ANTHROPIC_API_KEY="你的key"

python cr_cli.py \
  --svn-path J:/trunk \
  --revision 168540
