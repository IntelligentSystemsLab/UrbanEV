# UrbanEV

UrbanEV is an open dataset of EV charging space availability and electricity use in Shenzhen, China. This project is dedicated to the public domain using the [CC0 1.0 Universal License](LICENSE). For more information, see [Creative Commons - CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Citations

 If this project is helpful to your research, please cite our papers:

> Li, H., Qu, H., Tan, X. et al. (2025). UrbanEV: An Open Benchmark Dataset for Urban Electric Vehicle Charging Demand Prediction. Scientific Data. [Paper in Spring Nature](https://doi.org/10.1038/s41597-025-04874-4)

> Qu, H., Kuang, H., Li, J., & You, L. (2023). A physics-informed and attention-based graph learning approach for regional electric vehicle charging demand prediction. IEEE Transactions on Intellgent Transportation Systems. [Paper in IEEE Explore](https://ieeexplore.ieee.org/document/10539613) [Paper in arXiv](https://arxiv.org/abs/2309.05259)

> Kuang, H., Zhang, X., Qu, H., and You, L., and Zhu, R. and Li, J. (2024). Unravelling the effect of electricity price on electric vehicle charging behavior: A case study in Shenzhen, China. Sustainable Cities and Society. [DOI](https://doi.org/10.1016/j.scs.2024.105836)

> Haohao Qu, Han Li, Linlin You, Rui Zhu, Jinyue Yan, Paolo Santi, Carlo Ratti, Chau Yuen. (2024) ChatEV: Predicting electric vehicle charging demand as natural language processing. Transportation Research Part D: Transport and Environment. [Paper in TRD](https://doi.org/10.1016/j.trd.2024.104470) [Code in Github](https://github.com/Quhaoh233/ChatEV)

```shell
@article{li2025urbanev,
  author={Li, Han and Qu, Haohao and Tan, Xiaojun and You, Linlin and Zhu, Rui and Fan, Wenqi}
  title={UrbanEV: An Open Benchmark Dataset for Urban Electric Vehicle Charging Demand Prediction},
  journal={Scientific Data},
  volum={12},
  pages={523},
  year={2025},
  issn={2052-4463},
  doi={10.1038/s41597-025-04874-4},
}

@Article{qu2024a,
  author={Qu, Haohao and Kuang, Haoxuan and Wang, Qiuxuan and Li, Jun and You, Linlin},
  journal={IEEE Transactions on Intelligent Transportation Systems}, 
  title={A Physics-Informed and Attention-Based Graph Learning Approach for Regional Electric Vehicle Charging Demand Prediction}, 
  year={2024},
  pages={1-14},
  doi={10.1109/TITS.2024.3401850}}

@article{kuang2024unravelling,
  title={Unravelling the effect of electricity price on electric vehicle charging behavior: A case study in Shenzhen, China},
  author={Kuang, Haoxuan and Zhang, Xinyu and Qu, Haohao and You, Linlin and Zhu, Rui and Li, Jun},
  journal={Sustainable Cities and Society},
  pages={105836},
  year={2024},
  publisher={Elsevier}
}

@article{qu2024chatev,
 title = {ChatEV: Predicting electric vehicle charging demand as natural language processing},
 journal = {Transportation Research Part D: Transport and Environment},
 volume = {136},
 pages = {104470},
 year = {2024},
 issn = {1361-9209},
 author = {Haohao Qu and Han Li and Linlin You and Rui Zhu and Jinyue Yan and Paolo Santi and Carlo Ratti and Chau Yuen},
}
```

## Contact

If you have any questions regarding this dataset, feel free to reach out.

Author: Han Li [lihan76@mail2.sysu.edu.cn](lihan76@mail2.sysu.edu.cn), Haohao Qu [haohao.qu@connect.polyu.hk](haohao.qu@connect.polyu.hk)

## Updates

* January 19, 2025: Uploaded code and data for distribution prediction based on UrbanEV.
* March 17, 2025: Published the dataset on [Data in Dryad](https://doi.org/10.5061/dryad.np5hqc04z).
* March 28, 2025: The paper "UrbanEV: An Open Benchmark Dataset for Urban Electric Vehicle Charging Demand Prediction" was published in Scientific Data. [Paper in Spring Nature](https://doi.org/10.1038/s41597-025-04874-4)

## Data Description

The UrbanEV dataset was developed to meet the urgent need for understanding and forecasting electric vehicle (EV) charging demand in urban environments. As global EV adoption accelerates, efficient charging infrastructure management is crucial for ensuring grid stability and enhancing user experience. Collected from public EV charging stations in Shenzhen, China — a leading city in vehicle electrification — the dataset covers a six-month period (**September 1, 2022, to February 28, 2023**), capturing seasonal variations in charging patterns. To ensure data quality, the raw records underwent meticulous preprocessing, including the extraction of key information (availability status, rated power, and fees), anomaly removal, and missing value imputation via forward and backward filling. Outliers identified by the IQR method were replaced with adjacent valid values. The data was aggregated both temporally (hourly) and spatially (by traffic zones), with variance tests and zero-value filtering applied to exclude low-activity regions.The final dataset includes:

* **Charging data**: occupancy, duration, and volume
* **Environmental context**: weather conditions
* **Spatial features**: adjacency matrices, distances
* **Static attributes**: Points of Interest, area size, and road length

## Data Access

All datasets related to UrbanEV have been made publicly available on  **[Dryad](https://doi.org/10.5061/dryad.np5hqc04z)**. In addition to Dryad, all datasets are also available on **[Google Drive](https://drive.google.com/drive/folders/1VUgdb8uNgmtvO93BHBK_OrSxjndrF-48?usp=sharing)** and **[Baidu Netdisk](https://pan.baidu.com/s/1__-IjG39tz9VIhHVK3XpQw?pwd=1234#list/path=%2F)** for easier access and to host the most up-to-date versions of the datasets. This includes:

* Preprocessed **zone-level data** at both **hourly** and **5-minute** resolution (**1,362** charging stations with **17,532** charging piles)
* **Raw station-level data** at **5-minute** resolution (before preprocessing) (**1,682** charging stations with **24,798** charging piles)

The data directory of this GitHub repository contains the preprocessed zone-level dataset used in [Paper in Spring Nature](https://doi.org/10.1038/s41597-025-04874-4)

![avatar](figs/map.png) Figure 1. Spatial distribution of **1,682** public charging stations and **24,798** charging piles in the UrbanEV dataset.

## Files

**code**: Code for distribution time-series prediction using traditional models and deep learning models based on the UrbanEV dataset, including several modularized functions.

* `baselines.py`: Includes three traditional forecasting methods (Last Observation, Auto-regressive (AR), and ARIMA) and six deep learning models (Fully Connected Neural Network (FCNN), Long Short-Term Memory (LSTM), Graph Convolutional Network (GCN), GCN-LSTM, Attention-Based Spatial-Temporal Graph Convolutional Network (ASTGCN)).
* `exp.bat`|`exp.sh`: Scripts for distribution time-series prediction.
* `init_env.bat`|`init_env.sh`: Scripts to create a virtual environment for running time-series predictions based on the UrbanEV dataset.
* `main.py`: Main script file.
* `parse.py`: Provides a command-line interface to configure training parameters for spatiotemporal EV charging demand prediction models.
* `preprocess.py`: Converts data in the `./data/dataset` folder into a format suitable for training and predicting with Transformer-based time-series models.
* `train.py`: Model training script.
* `utils.py`: Utility functions related to the UrbanEV dataset predictions, e.g., time-series cross-validation and dataset preparation.

**data**:  1-hour resolution zone-level data of the UrbanEV dataset, which has been cleaned through outlier detection, zero-value checks, etc., and includes data from **275 zones**, **1,362 charging stations**, and **17,532 charging piles**.

* `adj.csv`: Adjacency matrix.
* `duration.csv`: Hourly EV charging duration (Unit: hour).
* `e_price.csv`: Electricity price (Unit: Yuan/kWh).
* `inf.csv`: Filtered station-level data for the 275 zones, including coordinates, charging capacities, area (Unit: m^2), and perimeter (Unit: m).
* `inf_raw.csv`: All station-level data for the same 275 zones, including coordinates, charging capacities, area (Unit: m^2), and perimeter (Unit: m).
* `occupancy.csv`: Hourly EV charging occupancy rate (Unit: %).
* `s_price.csv`: Service price (Unit: Yuan/kWh).
* `volume.csv`: Hourly EV charging volume (Unit: kWh). The volume in *volume.csv* is derived from the rated power of charging piles
* `volume-11kW.csv` provides an alternative vehicle-side estimation of charging volume to mitigate potential overestimation in `volume.csv`. Specifically, for direct current charging stations, the volume is calculated using the standard power of the most commonly used electric vehicle, Tesla Model Y (11kW), instead of the rated power of the charging pile.
* `weather_airport.csv`: Weather data from the meteorological station at Bao'an Airport (Shenzhen). These are the raw data collected, and it is recommended to use the **Max-Min** method for normalization.
* `weather_central.csv`: Weather data from Futian Meteorological Station in the city center of Shenzhen.
* `weather_header.txt`: Descriptions of the table headers in `weather_airport.csv` and `weather_central.csv`.
* `distance.csv`: Distance matrix between the 275 zones.
* `poi.csv`: Points of Interest categorized into three types: `food and beverage services`, `business and residential`, and `lifestyle services`. The coordinates used are based on the `WGS84` coordinate system.
* Notes: Our occupancy data is gathered from an availability perspective, while the duration and volume data is collected from a utilization standpoint. Specifically, the occupancy data records all unavailable or busy charging piles. In contrast, the duration and volume data only account for the piles actively providing electricity. You can select the data according to your research purpose.

**code_transformer**: Code for distribution time-series prediction using Transformer-based models on the UrbanEV dataset. Below are explanations for some core files and directories related to UrbanEV prediction:

* `dataset/st-evcdp`: Contains data files used for predictions, which can be generated through `../code/preprocess.py`.
* `exp.bat`|`exp.sh`: Scripts for distribution time-series prediction using Transformer-based models.

## Environment Requirements

This section outlines the setup for the virtual environment required for time-series prediction based on UrbanEV, using Python 3.8 and PyTorch 2.4.1. Assuming your working directory is the project root directory, here are the relevant commands:

Windows

```shell
cd code
init_env.bat
```

Linux

```shell
cd code
./init_env.sh
```

Due to the discontinuation of PyG Temporal, you may encounter a ModuleNotFoundError: No module named 'torch_geometric.utils.to_dense_adj' when running ASTGCN experiments. To resolve this, change from torch_geometric.utils.to_dense_adj import to_dense_adj to from torch_geometric.utils import to_dense_adj. See[pyg-#9023 (reply in thread)](https://github.com/pyg-team/pytorch_geometric/discussions/9023#discussioncomment-8813817) for more details.

## Run Distribution Prediction on the UrbanEV Dataset

All commands below assume your working directory is the **project root**. Start each session in the root directory. Some commands require moving into subdirectories (e.g., `cd code`, `cd code-transformer`) — you can return to the root using:

```shell
cd ..
```

Do this as needed before running the next block.

---

### Step 1: Environment Setup

```shell
conda activate UrbanEV
```

---

### Step 2: Preprocess Data (Only Once Needed)

```shell
cd code
python preprocess.py
```

> **Note:** Ensure data preprocessing is completed before running any models. `TimeXer` and `TimeNet` use different scripts than the other models.

---

### Step 3: Run Models

#### A. Statistical & Deep Learning Models (`ar`, `arima`, `fcnn`, `lstm`, `gcn`, `gcnlstm`, `astgcn`)

**Example (Single Run):**

```shell
cd code
python main.py --model fcnn --seq_len 12 --pred_len 3 --fold 1 --epoch 20
```

**To run all experiments:**

Run the appropriate script based on your operating system:

* **Linux:**

  ```shell
  cd code
  ./exp.sh
  ```
* **Windows:**

  ```shell
  cd code
  ./exp.bat
  ```

#### B. SOTA Time Series Models (`TimeXer`, `TimeNet`)

**Example (Single Run):**

```shell
cd code-transformer
python run.py --model TimeXer --seq_len 12 --epoch 1 --pred_len 3 --fold 1
```
> **Note:** Make sure that `label_len` is not greater than `seq_len`.

**To run all experiments:**

Run the appropriate script based on your operating system:

* **Linux:**

  ```shell
  cd code-transformer
  ./exp.sh
  ```
* **Windows:**

  ```shell
  cd code-transformer
  ./exp.bat
  ```


## Acknowledgement

The project is based on the following time series forecasting repositories, from which you can explore more about the models and methods by clicking on the respective links:

* Time Series Library (TSLib)：[https://github.com/thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library).
* PyG Temporal: [https://github.com/benedekrozemberczki/pytorch_geometric_temporal](https://github.com/benedekrozemberczki/pytorch_geometric_temporal)

More updates will be posed in the near future! Thank you for your interest.
