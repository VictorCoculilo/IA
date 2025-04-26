@echo off
echo === Criando ambiente virtual com Python 3.11 ===
py -3.11 -m venv venv

echo === Ativando o ambiente virtual ===
call venv\Scripts\activate.bat

echo === Indo para a pasta do autograder ===
cd src\search

echo === Rodando autograder com Python 3.11 ===
python autograder.py -q q1

echo === Voltando para a pasta raiz ===
cd ..\..

echo === Pressione qualquer tecla para encerrar ===
pause
