# Data Cleaning Project

### Getting Started

1. Start by cloning this repository to your local environment

```bash
git clone https://github.com/adithya-r-01/data-cleaning-project.git
```

2. The datasets used for the cleaning _are_ explicitly within this repository. Untar the `data.tar.gz` file for the datasets or download the datasets directly from [this link](https://uofi.app.box.com/s/zh2hxfkq0cc6vyftw91nqa4smdpq7ybk) and at minimum download the `Menu.csv`, `Dish.csv`, and `MenuItem.csv`.

3. After you have downloaded the csv files into a data directory in the same directory as the cloned local repository activate your `conda` environment to inject the dependencies required for this project. This can be done via the command below (assuming you have `conda`).

```bash
conda create --name datacleaningproj --file requirements.txt
```
```bash
conda activate datacleaningproj
```

4. Your local environment should now be setup to interact with the project

### Understanding The Notebooks

The notebooks provided are either responsible for performing the cleaning themselves or serve as benchmarks that _assess_ the cleaning performed.

`MenuCleaning.ipynb` tracks the full end-to-end cleaning of the `Menu.csv` dataset along with helpful annotations to understand how/why certain steps were performed.

`MenuItemCleaning.ipynb` tracks the full end-to-end cleaning of the `MenuItem.csv` dataset along with helpful annotations to understand how/why certain steps were performed.

`DataCleaningChanges.ipynb` was used to acquire quantitative metrics about _how_ the performed cleaning changes the underlying datasets i.e number of cells removed or modified.

`ICViolations.ipynb` assess the integrity constraints defined by the group against the cleaned dataset.
