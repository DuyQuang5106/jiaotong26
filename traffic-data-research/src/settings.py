"""Deterministic run configuration, without credentials or external evaluation."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
CONFIG=yaml.safe_load((ROOT/'config.yaml').read_text(encoding='utf-8'))
assert CONFIG['seed']==42, 'This documented run uses seed 42; update reports for other seeds.'
