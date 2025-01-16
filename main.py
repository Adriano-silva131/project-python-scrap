from sqlalchemy.orm import sessionmaker
from config import engine
from data import get_file_paths, extract_data_from_file, insert_data_to_db
import os


def main(directory_path):
    Session = sessionmaker(bind=engine)
    db = Session()

    processed_files = {}

    file_paths = get_file_paths(directory_path)
    for file_path in file_paths:
        modification_time = os.path.getmtime(file_path)
        processed_files[file_path] = modification_time

        extracted_data = extract_data_from_file(file_path)
        insert_data_to_db(db, extracted_data)


if __name__ == "__main__":
    main()
