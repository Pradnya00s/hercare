#!/usr/bin/env python
"""
Generate a CNN Model for PCOS Ultrasound Classification
========================================================

This script creates a valid CNN model for testing. You should replace this
with your actual trained model.

Run with:
    python generate_cnn_model.py
"""

import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def create_demo_cnn_model():
    """Create a simple but valid CNN model for ultrasound classification."""
    
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    
    print("\n" + "="*70)
    print("🧠 Generating CNN Model for PCOS Ultrasound Classification")
    print("="*70 + "\n")
    
    # Define model architecture
    print("1️⃣  Building model architecture...")
    
    model = keras.Sequential([
        # Input layer: 224x224x3 (RGB ultrasound images)
        layers.Input(shape=(224, 224, 3)),
        
        # First convolutional block
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Global average pooling
        layers.GlobalAveragePooling2D(),
        
        # Fully connected layers
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        
        # Output layer: binary classification (PCOS or Normal)
        layers.Dense(1, activation='sigmoid')
    ])
    
    print("   ✅ Model architecture created")
    print("\n   Model Summary:")
    print("   " + "-"*65)
    model.summary()
    print("   " + "-"*65)
    
    # Compile model
    print("\n2️⃣  Compiling model...")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    print("   ✅ Model compiled")
    
    # Test model with dummy data
    print("\n3️⃣  Testing model with synthetic data...")
    
    # Create synthetic training data
    X_dummy = np.random.rand(10, 224, 224, 3).astype(np.float32)
    y_dummy = np.random.randint(0, 2, 10).astype(np.float32)
    
    # Train for 2 epochs just to validate it works
    print("   Training on 10 synthetic ultrasound images for 2 epochs...")
    history = model.fit(
        X_dummy, y_dummy,
        epochs=2,
        batch_size=2,
        validation_split=0.2,
        verbose=0
    )
    print("   ✅ Model training successful")
    print(f"      Final training loss: {history.history['loss'][-1]:.4f}")
    print(f"      Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    
    # Test prediction
    print("\n4️⃣  Testing model prediction...")
    test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
    prediction = model.predict(test_input, verbose=0)
    print(f"   ✅ Prediction successful")
    print(f"      Input shape: {test_input.shape}")
    print(f"      Output shape: {prediction.shape}")
    print(f"      Prediction value: {prediction[0][0]:.4f}")
    print(f"      (Values between 0-1, where 1 = high PCOS probability)")
    
    return model


def save_model(model, output_path="pcos_screener/model/model.h5"):
    """Save the model to disk."""
    
    print(f"\n5️⃣  Saving model to {output_path}...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save model
    model.save(output_path)
    
    file_size = os.path.getsize(output_path)
    print(f"   ✅ Model saved successfully")
    print(f"      File size: {file_size / 1024 / 1024:.2f} MB")
    print(f"      Path: {os.path.abspath(output_path)}")
    
    return True


def verify_model(model_path="pcos_screener/model/model.h5"):
    """Verify the saved model can be loaded."""
    
    print(f"\n6️⃣  Verifying saved model...")
    
    from tensorflow import keras
    
    try:
        loaded_model = keras.models.load_model(model_path)
        print(f"   ✅ Model loaded successfully")
        print(f"      Input shape: {loaded_model.input_shape}")
        print(f"      Output shape: {loaded_model.output_shape}")
        
        # Test prediction with loaded model
        test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        prediction = loaded_model.predict(test_input, verbose=0)
        print(f"   ✅ Prediction with loaded model successful")
        print(f"      Test prediction: {prediction[0][0]:.4f}")
        
        return True
    except Exception as e:
        print(f"   ❌ Failed to load model: {e}")
        return False


def main():
    """Generate and save the CNN model."""
    
    print("\n" + "="*70)
    print("IMPORTANT NOTICE")
    print("="*70)
    print("""
This script generates a DEMO CNN MODEL for testing the HerCare system.

⚠️  This model is trained on SYNTHETIC DATA and is NOT suitable for 
    actual medical diagnosis. It's meant for:
    
    ✅ Testing the complete system workflow
    ✅ Validating API endpoints
    ✅ Development and debugging
    
❌ You MUST replace this with a real trained model before production use!

To use a real model:
    1. Train your CNN on actual ultrasound/PCOS dataset
    2. Save it as: pcos_screener/model/model.h5
    3. Model must accept 224x224x3 RGB images
    4. Output must be binary (0-1) probability for PCOS
    """)
    
    response = input("\nDo you want to generate the demo model? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Cancelled.")
        return 1
    
    # Generate model
    try:
        model = create_demo_cnn_model()
        
        # Save it
        if not save_model(model):
            return 1
        
        # Verify it
        if not verify_model():
            return 1
        
        print("\n" + "="*70)
        print("✅ Demo CNN Model Generated Successfully!")
        print("="*70)
        print("""
You can now:
1. Run the Django server: python manage.py runserver
2. Test the ultrasound upload in the frontend
3. Verify the complete system works end-to-end

Remember to replace this demo model with a properly trained model
before deploying to production!
""")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
