# 🩺 Skin Cancer Detection System

> *Early detection saves lives - Leveraging AI to identify potential skin cancer from lesion images*

## 📋 Overview

Skin cancer is one of the most common cancers worldwide. This system uses a **Convolutional Neural Network (CNN)** trained on skin lesion images to classify 9 different skin conditions.

### 🎯 Features

- 📤 Upload skin lesion images (JPG, JPEG, PNG)
- 🔍 AI-powered analysis using TensorFlow
- 📊 Confidence score with 70% threshold
- 🚨 Detects 4 types of skin cancer
- ✨ Beautiful GUI with animated background

### Detected Cancer Types

| Cancer Type | Status |
|-------------|--------|
| Actinic Keratosis | 🔴 CANCEROUS |
| Basal Cell Carcinoma | 🔴 CANCEROUS |
| Melanoma | 🔴 CANCEROUS |
| Squamous Cell Carcinoma | 🔴 CANCEROUS |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher

### Steps

1. **Install dependencies:**
```bash
pip install tensorflow pillow numpy