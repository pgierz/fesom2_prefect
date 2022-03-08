import os

import prefect
from git import Repo
from prefect import Flow, Parameter, task
from prefect.tasks.shell import ShellTask
from prefect.executors import LocalDaskExecutor


@task(log_stdout=True)
def download_fesom2(branch, local_location):
    local_location += "/fesom2"
    print(
        f"We will now download and compile FESOM2 for {branch} to {local_location}!"
    )
    Repo.clone_from(
        "https://github.com/FESOM/fesom2",
        multi_options=[
            f"-b {branch}",
        ],
        to_path=local_location,
    )
    return f"{local_location}"


@task(log_stdout=True)
def compile_fesom2_ogcm(fesom_folder):
    print(f"Compiling the FESOM 2 Ocean Model in {fesom_folder}")
    task = ShellTask(return_all=True, log_stderr=True, helper_script=f"module purge && module list && cd {fesom_folder}")
    compile_output = task.run(command="bash configure.sh")


@task(log_stdout=True)
def compile_fesom2_metis(fesom_folder):
    print("Compiling the METIS FESOM2 Mesh Partitioner")
    task = ShellTask(return_all=True, log_stderr=True, helper_script=f"module purge && module list && cd {fesom_folder}/mesh_part")
    compile_output = task.run(command="bash configure.sh")


with Flow("Compile Fesom2 Model") as compile_model_flow:
    branch = Parameter("Branch Name", default="master")
    local_location = Parameter("Supercomputer Directory", default=os.getcwd())
    fesom_folder = download_fesom2(branch, local_location)
    compile_fesom2_ogcm(fesom_folder)


with Flow("Compile Fesom2 Mesh Part") as compile_mesh_part_flow:
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
