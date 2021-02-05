#!/bin/zsh

GRIDCONTROL_DIR=$1
echo "checking directory:" $GRIDCONTROL_DIR

if test -f ${GRIDCONTROL_DIR}/cmssw-project-area.tar.gz;
then
  echo "directory is GRIDCONTROL folder - OK!"
else
  echo "directory is NOT GRIDCONTROL folder - FAILED!"
  return
fi

failed_datasets=()
for file in ${GRIDCONTROL_DIR}/output/*/job.info;
do
  exit_code_return=$(awk '/EXITCODE=/' $file)
  if [ "$exit_code_return" != "EXITCODE=0" ];
  then
    split_arr=($(echo $file | tr '/' '\n'))
    job_id_folder=$(echo ${split_arr[${#split_arr[@]} - 1]})
    echo $exit_code_return $job_id_folder

    # split_job_id=($(echo ${split_arr[${#split_arr[@]} - 1]} | tr '_' '\n'))
    # job_id=${split_job_id[${#split_job_id[@]}]}
    # echo $exit_code_return ${split_arr[${#split_arr[@]} - 1]} \-\> job ID: $job_id

    dataset=$(awk '/DATASETPATH=/' ${GRIDCONTROL_DIR}/output/${job_id_folder}/${job_id_folder}.var)
    failed_datasets+=$(expr $dataset : '.*"\(.*\)\".*')
  fi
done

echo "list of failed datasets (unique are printed):"
sorted_unique_ids=($(echo "${failed_datasets[@]}" | tr ' ' '\n' | sort -u ))
echo "${sorted_unique_ids[@]}" |  tr ' ' '\n'
