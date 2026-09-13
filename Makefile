.PHONY: check hardware-check detector-head-check power-interface-check

check:
	$(MAKE) --keep-going detector-head-check power-interface-check

hardware-check: check

detector-head-check:
	/usr/bin/python3 scripts/kicad-check.py \
		hardware/muon_detector_head/muon_detector_head \
		--profile hardware/muon_detector_head/validation.json \
		--output build/checks/detector-head

power-interface-check:
	/usr/bin/python3 scripts/kicad-check.py \
		hardware/power_interface/power_interface \
		--profile hardware/power_interface/validation.json \
		--output build/checks/power-interface
