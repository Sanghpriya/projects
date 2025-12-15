# Brain Tumor Classification from MRI using CNN–LSTM

This project presents a research-oriented deep learning pipeline for multi-class brain tumor classification from MRI images. The approach combines a pretrained CNN (ResNet18) for spatial feature extraction with an LSTM network to model spatial dependencies across ordered image patches, enabling robust discrimination among tumor types.

The model is evaluated on a four-class brain MRI dataset (glioma, meningioma, pituitary, and no-tumor) and achieves high discriminative performance, validated using precision, recall, F1-score, and multi-class ROC–AUC analysis.

## Key Characteristics:

Patch-based decomposition of MRI images to form spatial feature sequences

Frozen ResNet18 used as a feature extractor for reproducible experiments

RNN-LSTM classifier trained on extracted feature sequences for classification

Comprehensive evaluation using confusion matrix, macro-F1, and one-vs-rest ROC curves

Inference-ready pipeline with saved models and a Streamlit demo application


## About Dataset:

https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset

This dataset is a combination of the following three datasets :
figshare
SARTAJ dataset
Br35H
This dataset contains 7023 images of human brain MRI images which are classified into 4 classes: glioma - meningioma - no tumor and pituitary.
no tumor class images were taken from the Br35H dataset.
