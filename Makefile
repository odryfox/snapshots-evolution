up:
	PYTHONPATH=snapshots_evolution uvicorn web.app:app --reload

test:
	PYTHONPATH=snapshots_evolution python -m pytest -c snapshots_evolution/pytest.ini
