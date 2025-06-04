#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh
conda activate madlibs

export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export DATASET_NAME="./madlibs_images"

accelerate launch --mixed_precision="no" train_text_to_image_lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$DATASET_NAME --caption_column="text" \
  --resolution=512 --random_flip \
  --train_batch_size=1 \
  --num_train_epochs=100 --checkpointing_steps=5000 \
  --learning_rate=1e-04 --lr_scheduler="constant" --lr_warmup_steps=0 \
  --seed=42 \
  --output_dir="sd-madlibs-model-lora" \
  --validation_prompt="character playing the guitar" --report_to="wandb"
