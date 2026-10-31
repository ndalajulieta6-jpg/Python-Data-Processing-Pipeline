from src.pipeline.pipeline import DataPipeline

if __name__ == "__main__":
    pipeline = DataPipeline("config/config.yaml")
    result = pipeline.run()
    print(f"Pipeline complete: {result}")
