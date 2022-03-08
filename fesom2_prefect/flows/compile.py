import os

import prefect
from git import Repo
from prefect import Flow, Parameter, task
from prefect.tasks.shell import ShellTask
from prefect.executors import LocalDaskExecutor

with Flow("Compile Fesom2 Model", executor=LocalDaskExecutor()) as compile_model_flow:
    branch = Parameter("Branch Name", default="master")
    local_location = Parameter("Supercomputer Directory", default=os.getcwd())
    fesom_folder = download_fesom2(branch, local_location)
    compile_fesom2_ogcm(fesom_folder)


with Flow(
    "Compile Fesom2 Mesh Part", executor=LocalDaskExecutor()
) as compile_mesh_part_flow:
    branch = Parameter("Branch Name", default="master")
    local_location = Parameter("Supercomputer Directory", default=os.getcwd())
    fesom_folder = download_fesom2(branch, local_location)
    compile_fesom2_metis(fesom_folder)


with Flow("Compile Fesom2 All", executor=LocalDaskExecutor()) as compile_all_flow:
    branch = Parameter("Branch Name", default="master")
    local_location = Parameter("Supercomputer Directory", default=os.getcwd())
    fesom_folder = download_fesom2(branch, local_location)
    compile_fesom2_ogcm(fesom_folder)
    compile_fesom2_metis(fesom_folder)
