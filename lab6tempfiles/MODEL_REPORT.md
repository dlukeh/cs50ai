
```
MODEL_REPORT.md

---

# 📘 **Traffic Sign Classifier — Model Behavior Report**

## **1. Overview**
This report summarizes the behavior of a convolutional neural network (CNN) trained to classify German traffic signs using the GTSRB dataset.  
The model was trained on CPU and achieved **99.47% test accuracy**, with **28 misclassified images** out of thousands.

The goal is to document performance, identify patterns in misclassifications, and outline potential improvements.

---

## **2. Model Architecture**
The CNN consists of the following layers:

- **Conv2D (32 filters, 3×3, ReLU)**  
- **MaxPooling2D (2×2)**  
- **Conv2D (64 filters, 3×3, ReLU)**  
- **Conv2D (128 filters, 3×3, ReLU)**  
- **MaxPooling2D (2×2)**  
- **Flatten**  
- **Dense (128 units, ReLU)**  
- **Dropout (0.5)**  
- **Dense (NUM_CATEGORIES, softmax)**  

This architecture balances feature extraction, depth, and regularization.

---

## **3. Training Performance**

| Metric | Value |
|--------|--------|
| Training accuracy | ~0.97–0.98 |
| Training loss | ~0.09 |
| Test accuracy | **0.9947** |
| Test loss | 0.0331 |
| Misclassified images | **28** |

The model shows strong generalization with minimal overfitting.

---

## **4. Misclassification Analysis**
A total of **28 images** were misclassified.  
Visual inspection reveals several consistent patterns:

### **A. Visually Similar Classes**
Speed limits such as **50, 60, 80** share:

- identical shapes  
- identical colors  
- similar internal patterns  

These are common confusion points in GTSRB.

### **B. Low-Quality Inputs**
Some misclassified images exhibit:

- motion blur  
- low resolution  
- compression artifacts  

These degrade key features needed for classification.

### **C. Rotated or Tilted Signs**
Signs photographed at an angle reduce clarity of:

- numbers  
- edges  
- internal symbols  

Rotation is a known weakness without augmentation.

### **D. Lighting Issues**
A few images show:

- glare  
- shadows  
- uneven brightness  

This can obscure critical features.

### **E. Partial Occlusion**
Some signs are partially blocked by:

- trees  
- poles  
- vehicles  

This reduces the visible feature set.

---

## **5. Strengths of the Model**

- High accuracy across all categories  
- Robust to moderate noise and variation  
- Learns shape‑based and color‑based features effectively  
- Strong performance without GPU acceleration  
- Stable training curve with no divergence  

---

## **6. Limitations**

- Sensitive to rotation  
- Sensitive to severe blur  
- Confuses visually similar speed limits  
- No data augmentation used  
- No transfer learning used  

These are expected limitations for a CNN trained from scratch.

---

## **7. Potential Improvements**

### **A. Add Data Augmentation**
Improves robustness to rotation, brightness shifts, zoom, and blur.

Example:

```python
tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    brightness_range=[0.8, 1.2],
    zoom_range=0.1,
    shear_range=0.1
)
```

### **B. Use Transfer Learning**
Models like MobileNetV2 or EfficientNetB0 can push accuracy above **99.8%**.

### **C. Add Batch Normalization**
Improves stability and convergence.

### **D. Increase Model Depth**
A third convolutional block could help with fine‑grained distinctions.

### **E. Use a Learning Rate Scheduler**
Helps refine the final epochs.

---

## **8. Conclusion**
The model performs exceptionally well, achieving **99.47% accuracy** and only **28 misclassifications**.  
The errors align with known challenges in traffic sign recognition and can be mitigated with augmentation or transfer learning.

This experiment demonstrates strong understanding of CNN design, training, and evaluation — and provides a solid foundation for more advanced deep learning and agent‑based projects.

---
