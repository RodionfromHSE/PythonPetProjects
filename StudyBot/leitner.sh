#!/bin/bash

STUDY_BOT_DIR="/Users/Rodion.Khvorostov/Desktop/Prog/Other/pet_projects/StudyBot"

echo "Starting Leitner System..."
python3 $STUDY_BOT_DIR/SmartishTerminal.py \
    --config $STUDY_BOT_DIR/config.yaml
echo "Leitner System Finished."
