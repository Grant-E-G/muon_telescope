.PHONY: check hardware-check detector-head-check power-interface-check

# pcbnew ships with KiCad's own Python on macOS; Debian/Ubuntu use the system Python.
PYTHON ?= $(firstword $(wildcard /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3) /usr/bin/python3)

check:
	$(MAKE) --keep-going detector-head-check power-interface-check

hardware-check: check

detector-head-check:
	$(PYTHON) scripts/kicad-check.py \
		hardware/muon_detector_head/muon_detector_head \
		--profile hardware/muon_detector_head/validation.json \
		--output build/checks/detector-head

power-interface-check:
	$(PYTHON) scripts/kicad-check.py \
		hardware/power_interface/power_interface \
		--profile hardware/power_interface/validation.json \
		--output build/checks/power-interface
