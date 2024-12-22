from src.elts import ApiExtractor, StgToDdsLoader
from src.scripts.create_db import init_db

if __name__ == "__main__":
    init_db()

    api_extractor = ApiExtractor()
    api_extractor.run()

    stg_to_dds_loader = StgToDdsLoader()
    stg_to_dds_loader.run()
