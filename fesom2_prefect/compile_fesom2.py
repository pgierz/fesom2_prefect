import os

from git import Repo
from prefect import Flow, Parameter, task
from prefect.tasks.shell import ShellTask


@task
def download_fesom2(branch, local_location):
    local_location += "/fesom2"
    print(
        f"We will now download and compile FESOM2 for {branch} to {local_location}/fesom2!"
    )
    Repo.clone_from(
        "https://github.com/FESOM/fesom2",
        multi_options=[
            f"-b {branch}",
        ],
        to_path=local_location,
    )
    return local_location


@task
def compile_fesom2_ogcm(fesom_folder):
    print("Compiling the main FESOM2 Model")
    task = ShellTask(helper_script=f"cd {fesom_folder}/fesom2")
    modules_loaded = task.run("module list", return_all=True)
    print(modules_loaded)


@task
def compile_fesom2_metis(fesom_folder):
    print("Compiling the METIS FESOM2 Mesh Partitioner")


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


with Flow("Compile Fesom2 All") as compile_all_flow:
    branch = Parameter("Branch Name", default="master")
    local_location = Parameter("Supercomputer Directory", default=os.getcwd())
    fesom_folder = download_fesom2(branch, local_location)
    compile_fesom2_ogcm(fesom_folder)
    compile_fesom2_metis(fesom_folder)
