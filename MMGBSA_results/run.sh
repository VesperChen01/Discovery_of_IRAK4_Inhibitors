#!/bin/bash


base_dir="/home/IRAK4/output/"
mmpbsa_file="/home/IRAK4/mmpbsa.in"


if [ ! -f "$mmpbsa_file" ]; then
    echo "Error: mmpbsa.in file not found at $mmpbsa_file"
    exit 1
fi


for dir in "$base_dir"/*; do
    if [ -d "$dir" ]; then
        echo "Checking directory: $dir"

       
        md_run_base="$dir/md_files/md_run"

       
        if [ -d "$md_run_base" ]; then
            for sub_dir in "$md_run_base"/*; do
               
                if [ -d "$sub_dir" ]; then
                    echo "Processing: $sub_dir"

               
                    unique_suffix=$(basename "$sub_dir")

                
                    run_gbsa --wdir_to_run "$sub_dir" -c 1 -m "$mmpbsa_file" \
                        --out_suffix "$unique_suffix" > "$sub_dir/run_gbsa_$unique_suffix.log" 2>&1
                else
                    echo "Skipping: $sub_dir is not a directory"
                fi
            done
        else
            echo "md_run directory not found in: $dir"
        fi
    fi
done
