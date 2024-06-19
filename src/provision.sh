echo "Hej from FreeBSD user!"

pyenv update

echo "Installing Python 3.12.1"
pyenv install 3.12-dev
echo "Installing Python 3.13-dev"
pyenv install 3.13-dev

echo 'export PYENV_ROOT="$HOME/.pyenv/shims"' >> /home/freebsd/.bashrc
echo 'export PATH="$PYENV_ROOT:$PATH"' >> /home/freebsd/.bashrc
echo 'export PIPENV_PYTHON="$PYENV_ROOT/python"' >> /home/freebsd/.bashrc

#echo 'eval "$(pyenv init -)"' >> /home/freebsd/.bash_profile
#source /home/freebsd/.bashrc

mkdir pip_dependencies
cd pip_dependencies
wget https://files.pythonhosted.org/packages/30/6d/6de6be2d02603ab56e72997708809e8a5b0fbfee080735109b40a3564843/Jinja2-3.1.3-py3-none-any.whl
wget https://files.pythonhosted.org/packages/c3/fc/254c3e9b5feb89ff5b9076a23218dafbc99c96ac5941e900b71206e6313b/werkzeug-3.0.1-py3-none-any.whl
wget https://files.pythonhosted.org/packages/bd/0e/63738e88e981ae57c23bad6c499898314a1110a4141f77d7bd929b552fb4/flask-3.0.1-py3-none-any.whl
wget https://files.pythonhosted.org/packages/fb/5a/fb1326fe32913e663c8e2d6bdf7cde6f472e51f9c21f0768d9b9080fe7c5/MarkupSafe-2.1.4.tar.gz
wget https://files.pythonhosted.org/packages/c0/8b/d8427f023c081a8303e6ac7209c16e6878f2765d5b59667f3903fbcfd365/importlib_metadata-7.0.1-py3-none-any.whl
wget https://files.pythonhosted.org/packages/68/5f/447e04e828f47465eeab35b5d408b7ebaaaee207f48b7136c5a7267a30ae/itsdangerous-2.1.2-py3-none-any.whl
wget https://files.pythonhosted.org/packages/fa/2a/7f3714cbc6356a0efec525ce7a0613d581072ed6eb53eb7b9754f33db807/blinker-1.7.0-py3-none-any.whl
wget https://files.pythonhosted.org/packages/00/2e/d53fa4befbf2cfa713304affc7ca780ce4fc1fd8710527771b58311a3229/click-8.1.7-py3-none-any.whl
wget https://files.pythonhosted.org/packages/d9/66/48866fc6b158c81cc2bfecc04c480f105c6040e8b077bc54c634b4a67926/zipp-3.17.0-py3-none-any.whl
wget https://files.pythonhosted.org/packages/ec/1a/610693ac4ee14fcdf2d9bf3c493370e4f2ef7ae2e19217d7a237ff42367d/packaging-23.2-py3-none-any.whl
wget https://files.pythonhosted.org/packages/0e/2a/c3a878eccb100ccddf45c50b6b8db8cf3301a6adede6e31d48e8531cab13/gunicorn-21.2.0-py3-none-any.whl
cd ..

mkdir minitwit38
mkdir minitwit39
mkdir minitwit310
mkdir minitwit311
mkdir minitwit312
mkdir minitwit313

cd minitwit38
python3.8 -m venv .
source bin/activate
./bin/pip3.8 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.8 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.8 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..

cd minitwit39
python3.9 -m venv .
source bin/activate
./bin/pip3.9 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.9 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.9 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..

cd minitwit310
python3.10 -m venv .
source bin/activate
./bin/pip3.10 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.10 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.10 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..

cd minitwit311
python3.11 -m venv .
source bin/activate
./bin/pip3.11 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.11 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.11 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..

cd minitwit312
pyenv local 3.12-dev
python3.12
python3.12 -m venv .
source bin/activate
./bin/pip3.12 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.12 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.12 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..

cd minitwit313
pyenv local 3.13-dev
python3.13 -m venv .
source bin/activate
./bin/pip3.13 install ../pip_dependencies/MarkupSafe-2.1.4.tar.gz
./bin/pip3.13 install ../pip_dependencies/werkzeug-3.0.1-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/Jinja2-3.1.3-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/importlib_metadata-7.0.1-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/itsdangerous-2.1.2-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/blinker-1.7.0-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/click-8.1.7-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/zipp-3.17.0-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/flask-3.0.1-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/packaging-23.2-py3-none-any.whl
./bin/pip3.13 install ../pip_dependencies/gunicorn-21.2.0-py3-none-any.whl
deactivate
cd ..