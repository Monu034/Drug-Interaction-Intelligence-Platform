# SHARED: Model wrapper for binary serialization stability
class PredictionWrapper:
    def __init__(self, pipeline, encoder):
        self.pipeline = pipeline
        self.encoder = encoder
    def predict(self, X):
        y_encoded = self.pipeline.predict(X)
        return self.encoder.inverse_transform(y_encoded)
