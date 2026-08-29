#!/bin/sh
set -eu

required_version="9.0.9"
output_dir="build/checks"

if command -v kicad-cli >/dev/null 2>&1; then
    kicad_cli="kicad-cli"
elif [ -x "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]; then
    kicad_cli="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
else
    echo "error: kicad-cli ${required_version} is required" >&2
    exit 2
fi

installed_version="$("${kicad_cli}" --version)"
case "${installed_version}" in
    "${required_version}"*) ;;
    *)
        echo "error: KiCad ${required_version} is locked; found ${installed_version}" >&2
        exit 2
        ;;
esac

projects="hardware/detector_head/detector_head hardware/power_interface/power_interface"
for project in ${projects}; do
    for suffix in kicad_pro kicad_sch kicad_pcb; do
        if [ ! -f "${project}.${suffix}" ]; then
            echo "error: missing ${project}.${suffix}" >&2
            exit 2
        fi
    done
done

mkdir -p "${output_dir}"

for project in ${projects}; do
    name="$(basename "${project}")"
    "${kicad_cli}" sch erc \
        --severity-all \
        --exit-code-violations \
        --output "${output_dir}/${name}-erc.rpt" \
        "${project}.kicad_sch"
    "${kicad_cli}" pcb drc \
        --schematic-parity \
        --severity-all \
        --exit-code-violations \
        --output "${output_dir}/${name}-drc.rpt" \
        "${project}.kicad_pcb"
done

echo "Hardware checks passed with KiCad ${required_version}."
