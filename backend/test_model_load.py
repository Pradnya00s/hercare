#!/usr/bin/env python
"""
Test Script: Load and Inspect CNN Model
========================================
This script attempts to load the CNN model and shows detailed error information.

Run with:
    python test_model_load.py
"""

import os
import sys
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

def test_model_load():
    """Attempt to load the CNN model and show detailed information."""
    
    print("\n" + "="*60)
    print("🧪 Testing CNN Model Load")
    print("="*60 + "\n")
    
    # support either a .h5 file or a SavedModel folder
    default_h5 = "pcos_screener/model/model.h5"
    alternate_h5 = "pcos_screener/model/pcosmodel.h5"
    saved_dir = "pcos_screener/model/pcos_ultrasound_model"
    # choose whichever exists
    # pick H5 files first if available
    if os.path.exists(default_h5):
        model_path = default_h5
        print(f"1️⃣  Using HDF5 file: {model_path}")
    elif os.path.exists(alternate_h5):
        model_path = alternate_h5
        print(f"1️⃣  Using alternate HDF5 file: {model_path}")
    elif os.path.isdir(saved_dir):
        model_path = saved_dir
        print(f"1️⃣  Using SavedModel directory: {model_path}")
    else:
        model_path = default_h5
        print(f"1️⃣  Default path chosen: {model_path} (missing!)")
    
    abs_path = os.path.abspath(model_path)
    print(f"   Absolute path: {abs_path}")
    
    if not os.path.exists(model_path):
        print(f"   ❌ Model path does not exist")
        return False
    
    if os.path.isfile(model_path):
        size = os.path.getsize(model_path)
        print(f"   ✅ File exists ({size} bytes = {size/1024:.2f} KB)")
    else:
        print(f"   ✅ Directory exists (SavedModel format)")
    
    # Try importing TensorFlow
    print(f"\n2️⃣  Importing TensorFlow...")
    try:
        import tensorflow as tf
        from tensorflow import keras
        print(f"   ✅ TensorFlow {tf.__version__} imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import TensorFlow: {e}")
        return False
    
    # Try loading the model
    print(f"\n3️⃣  Loading model from {model_path}")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if os.path.isdir(model_path):
                print("   ▶ Detected SavedModel directory; attempting to load")
                from tensorflow import keras as tfkeras
                try:
                    print("   • trying TFSMLayer wrapper")
                    tfsmlayer = tfkeras.layers.TFSMLayer(model_path, call_endpoint="serving_default")
                    inp = tfkeras.Input(shape=(224,224,3))
                    model = tfkeras.Model(inputs=inp, outputs=tfsmlayer(inp))
                except Exception as e_wr:
                    print(f"   ⚠️ TFSMLayer failed: {e_wr}")
                    print("   • falling back to tf.saved_model.load")
                    import tensorflow as tf
                    loaded = tf.saved_model.load(model_path)
                    sigs = loaded.signatures
                    if 'serving_default' in sigs:
                        infer = sigs['serving_default']
                    else:
                        infer = list(sigs.values())[0]
                    class SMW:
                        def __init__(self, inf):
                            self._infer = inf
                        def predict(self, x, verbose=0):
                            import tensorflow as tf
                            _x = tf.convert_to_tensor(x)
                            out = self._infer(_x)
                            return list(out.values())[0].numpy()
                    model = SMW(infer)
            else:
                model = keras.models.load_model(model_path)
        
        print(f"   ✅ Model loaded successfully")
        
        # Show model info
        print(f"\n   Model Architecture:")
        print(f"   - Input shape: {model.input_shape}")
        print(f"   - Output shape: {model.output_shape}")
        print(f"   - Number of layers: {len(model.layers)}")
        print(f"   - Number of parameters: {model.count_params():,}")
        
        print(f"\n   Model Summary:")
        model.summary()
        
        # Try a test prediction
        print(f"\n4️⃣  Testing model prediction...")
        try:
            import numpy as np
            # Create a dummy input matching model input shape
            if model.input_shape[0] is None:
                # Batch size is None, so add it
                test_input_shape = (1,) + model.input_shape[1:]
            else:
                test_input_shape = model.input_shape
            
            print(f"   Test input shape: {test_input_shape}")
            test_input = np.random.rand(*test_input_shape).astype(np.float32)
            
            prediction = model.predict(test_input, verbose=0)
            print(f"   ✅ Test prediction successful")
            print(f"   - Output shape: {prediction.shape}")
            print(f"   - Output value(s): {prediction}")
            
        except Exception as e:
            print(f"   ❌ Test prediction failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to load model: {type(e).__name__}: {e}")
        import traceback
        print(f"\n   Full Traceback:")
        print(traceback.format_exc())
        
        # Try to give more specific advice
        if "% " in str(e) or "NoneType" in str(e):
            print(f"\n   💡 Hint: This error suggests the model file might be corrupted")
            print(f"           or in an incompatible format.")
        
        return False


def test_image_preprocessing():
    """Test image preprocessing."""
    
    print("\n" + "="*60)
    print("🖼️  Testing Image Preprocessing")
    print("="*60 + "\n")
    
    try:
        from PIL import Image
        import numpy as np
        
        print("1️⃣  Creating test image...")
        # Create a test image (224x224x3)
        test_image = Image.new('RGB', (224, 224), color='red')
        test_path = "/tmp/test_ultrasound.jpg"
        test_image.save(test_path)
        print(f"   ✅ Test image created: {test_path}")
        
        print("\n2️⃣  Testing preprocessing...")
        from pcos_screener.ultrasound_predict import preprocess_image
        
        processed = preprocess_image(test_path)
        print(f"   ✅ Image preprocessed successfully")
        print(f"   - Output shape: {processed.shape}")
        print(f"   - Output dtype: {processed.dtype}")
        print(f"   - Min value: {processed.min():.4f}, Max value: {processed.max():.4f}")
        
        if processed.min() >= -1 and processed.max() <= 1:
            print(f"   ✅ Values properly normalized to [-1, 1]")
        else:
            print(f"   ⚠️  Values outside expected range [-1, 1]")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Preprocessing test failed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False


def main():
    """Run all tests."""
    
    model_ok = test_model_load()
    preprocessing_ok = test_image_preprocessing()
    
    print("\n" + "="*60)
    print("📋 Test Summary")
    print("="*60 + "\n")
    
    if model_ok and preprocessing_ok:
        print("✅ All tests passed! The model is working correctly.")
        print("\nYou can now run the Django server:")
        print("   python manage.py runserver")
        return 0
    else:
        print("❌ Some tests failed. See above for details.")
        
        if not model_ok:
            print("\n⚠️  Model Loading Issue:")
            print("   - The model.h5 file might be corrupted")
            print("   - Try re-downloading or retraining the model")
            print("   - Check if the file is actually a valid TensorFlow/Keras model")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
