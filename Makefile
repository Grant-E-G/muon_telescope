.PHONY: check hardware-check

check: hardware-check

hardware-check:
	/usr/bin/python3 scripts/kicad-check.py \
		hardware/muon_detector_head/muon_detector_head \
		--profile hardware/muon_detector_head/validation.json
