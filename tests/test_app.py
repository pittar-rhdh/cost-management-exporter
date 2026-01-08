# test_app.py
import subprocess
import sys

def test_app_output():
    # Run the app.py script as a subprocess
    result = subprocess.run(
        [sys.executable, "app.py"],
        capture_output=True,
        text=True
    )
    
    # Assertions
    assert result.returncode == 0
    assert "Hello, World!" in result.stdout
    assert "Python 3.12" in result.stdout