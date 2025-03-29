# Dynamic Hackathon Project - Team Arjun (Team Number 348)

## Team Members
- Viren Mehta
- Karan Patel
- Perin Modi
- Shrey Patel

---

## Introduction
This project is designed for collision avoidance in multi-crane environments. The system utilizes machine learning models to detect and track persons near crane jibs to prevent accidents. The implementation includes dataset creation, training models, and a GUI-based simulation for real-time detection and tracking.

The model trained is **YOLOv8**, achieving an accuracy of **96%**.

---

## How to Use the Code
Follow these steps to use and run the project:

### 1. Setup Environment
Ensure you have Python installed along with necessary dependencies. Install the required packages using:
```bash
pip install -r requirements.txt
```

### 2. Dataset Creation
Run the `dataset_creation.ipynb` notebook to generate and preprocess the dataset for training.

### 3. Train the Model
Use `jib-person-training.ipynb` to train the model for detecting people near crane jibs.

### 4. Person Detection & Tracking
- Run `person_detect.ipynb` to detect people in the crane operation area.
- Use `person_tracker.ipynb` to track their movement.

### 5. Collision Avoidance Simulation
Run the `collision_avoidance_multicrane.py` script to visualize crane operations, restricted zones, and collision warnings using a Tkinter-based GUI.

```bash
python collision_avoidance_multicrane.py
```

### 6. Video Playback Prototype
Use `prototype_video_gui.py` to play prototype demonstration videos in a Tkinter-based player.

```bash
python prototype_video_gui.py
```

---

## Project Resources
- **PPT:** [View Here](https://drive.google.com/file/d/13RZ3N6_CE6rC5yR79IJqwghZQpjn2l__/view?usp=sharing)
- **Demo Video:** [Watch Here](https://drive.google.com/file/d/1iwivUbyUCCVZnp-K-Nn1iFfwkaStvSFl/view?usp=sharing)

---

## Contact
- **Viren Mehta:** [LinkedIn](https://www.linkedin.com/in/viren-mehta-0b14b8227/)
- **Karan Patel:** [LinkedIn](https://www.linkedin.com/in/karanpatel08/)
- **Perin Modi:** [LinkedIn](https://www.linkedin.com/in/modiperin/)
- **Shrey Patel:** [LinkedIn](https://www.linkedin.com/in/shreypatel07/)

---

**Developed for Dynamic Hackathon 2025 - Team Arjun (348).**

