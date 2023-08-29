#!/bin/bash

export CUDA_AVAILABLE_DEVICES=0,1

#export MAX_LENGTH=164
#export BERT_MODEL=distilbert-base-multilingual-cased
#export OUTPUT_DIR=distilbert_masakhaner
#export TEXT_RESULT=test_result.txt
#export TEXT_PREDICTION=test_predictions.txt
#export BATCH_SIZE=32
#export NUM_EPOCHS=50
#export SAVE_STEPS=10000
#export SEED=1

python3 train_ner.py --data_dir $DATA_DIR \
--model_type bert \
--model_name_or_path $MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict \
--overwrite_output_dir