module load apptainer
export AF3_RESOURCES_DIR=/pi/summer.thyme-umw/alphafold3
export AF3_IMAGE=${AF3_RESOURCES_DIR}/alphafold3_cuda7.sif
export AF3_CODE_DIR=${AF3_RESOURCES_DIR}/code
export AF3_INPUT_DIR=/pi/summer.thyme-umw/2024_intern_lab_space/thyme_lab_internship_2024/alphafold3/cxcr4/af_input
export AF3_OUTPUT_DIR=/pi/summer.thyme-umw/2024_intern_lab_space/thyme_lab_internship_2024/alphafold3/cxcr4/af_output
export AF3_MODEL_PARAMETERS_DIR=${AF3_RESOURCES_DIR}/params
export AF3_DATABASES_DIR=${AF3_RESOURCES_DIR}/db

apptainer exec \
     --nv \
     --env XLA_PYTHON_CLIENT_PREALLOCATE=false,TF_FORCE_UNIFIED_MEMORY=true,XLA_CLIENT_MEM_FRACTION=3.2 \
     --bind $AF3_INPUT_DIR:/root/af_input \
     --bind $AF3_OUTPUT_DIR:/root/af_output \
     --bind $AF3_MODEL_PARAMETERS_DIR:/root/models \
     --bind $AF3_DATABASES_DIR:/root/public_databases \
     $AF3_IMAGE \
     python ${AF3_CODE_DIR}/alphafold3/run_alphafold.py --run_inference=FALSE --flash_attention_implementation=xla \
     --json_path=/root/af_input/cxcr4_protein_only.json \
     --model_dir=/root/models \
     --db_dir=/root/public_databases \
     --output_dir=/root/af_output\








