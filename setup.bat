@echo off

echo Installing backend dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Installing frontend dependencies...
pushd frontend
if exist package-lock.json (
  npm ci
) else (
  npm install
)

REM Create .env.local if missing with a sensible default API URL
if not exist .env.local (
  echo NEXT_PUBLIC_API_URL=http://localhost:8000> .env.local
)
popd

echo Setup complete!
