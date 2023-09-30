robocopy /move /e PatroCar\img .\img
robocopy /move /e PatroCar\Training .\Training
pip install -e PatroCar
robocopy /move /e .\img PatroCar\img
robocopy /move /e .\Training PatroCar\Training